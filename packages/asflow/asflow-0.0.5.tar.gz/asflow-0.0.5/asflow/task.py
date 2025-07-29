import asyncio
import contextlib
import contextvars
import hashlib
import inspect
import os
import threading
import time
import traceback
from collections.abc import Callable
from dataclasses import dataclass
from functools import cached_property, wraps
from pathlib import Path
from typing import Any

from .compressor import create_compressor
from .retry import Retry
from .serializer import create_serializer


class TaskProgress:
    def __init__(self, progress, *args, **kwargs):
        self.progress = progress
        self.args = args
        self.kwargs = kwargs
        self.task_id = None

    def __enter__(self):
        if self.task_id is None:
            self.task_id = self.progress.add_task(*self.args, **self.kwargs)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.task_id:
            self.progress.remove_task(self.task_id)
            self.task_id = None

    def advance(self, advance=1):
        self.progress.advance(self.task_id, advance)

    def update(self, **kwargs):
        self.progress.update(self.task_id, **kwargs)


class Task:
    run_var = contextvars.ContextVar("@task")

    class Skipped(Exception):
        pass

    class Canceled(Exception):
        pass

    def __init__(self, flow):
        self.flow = flow

    def __call__(self, func=None, **kwargs):
        if func is None:
            # @flow.task(**kwargs)
            return TaskConfig(self, **kwargs).decorator
        else:
            # @flow.task
            return TaskConfig(self).decorator(func)

    @property
    def run(self):
        return Task.run_var.get()

    def progress(self, description=None, **kwargs):
        if task_progress := self.run._progress:
            if description is not None:
                kwargs["description"] = self.flow.run.TASKRUN_FORMAT.format(desc=description)
            task_progress.update(**kwargs)
            return task_progress

    def write(self, data):
        if task_run := self.run:
            if task_run.canceled:
                raise Task.Canceled()
            task_run.writer.write(task_run.config.serializer.encode(data))


class TaskConfig:
    def __init__(
        self,
        task,
        on=None,
        serializer=None,
        compressor=None,
        skip=(),
        suppress=(),
        retry=None,
        retry_exceptions=(Exception,),
        limit=None,
    ):
        self.task = task
        self.skip = skip
        self.suppress = suppress
        self.retry = retry
        self.retry_exceptions = retry_exceptions
        self.limit = limit if limit is not None else os.cpu_count()

        # writer
        if on:
            self.location = self.normalize_location(on)
            path = Path(self.location)
            self.serializer = create_serializer(path, serializer)
            self.compressor = create_compressor(path, compressor)
        else:
            self.location = None
            self.serializer = None
            self.compressor = None

    def normalize_location(self, pattern: str) -> str:
        if "://" in pattern:
            raise NotImplementedError(pattern)

        path = self.task.flow.path(pattern)

        # Replace "*" by "{hash}"
        match path.name.count("*"):
            case 0:
                pass
            case 1:
                path = path.with_name(path.name.replace("*", "{hash}"))
            case _:
                raise ValueError("too many wildcard", pattern)

        # Make sure the parent directory exists
        # Note: Executed at loading time to catch errors earlier
        path.parent.mkdir(parents=True, exist_ok=True)

        return str(path)

    def decorator(self, func):
        # Check async
        is_async = False
        if asyncio.iscoroutinefunction(func):
            # async def functions
            is_async = True
        elif callable(func) and asyncio.iscoroutinefunction(func.__call__):
            # async callable object like joblib.memory.AsyncMemorizedFunc
            is_async = True

        # Semaphore
        if self.limit:
            if is_async:
                self.semaphore = asyncio.BoundedSemaphore(self.limit)
            else:
                self.semaphore = threading.BoundedSemaphore(self.limit)
        else:
            self.semaphore = None

        # retry
        match self.retry:
            case None:

                def retry(func):
                    return func
            case int():
                retry = Retry(total=self.retry, exceptions=self.retry_exceptions)
            case Retry():
                retry = self.retry
            case _:
                raise TypeError(self.retry)

        if is_async:

            @wraps(func)
            @retry
            async def async_task_wrapper(*args, **kwargs):
                try:
                    async with TaskRun(self, func, args, kwargs) as run:
                        token = Task.run_var.set(run)
                        try:
                            return await func(*args, **kwargs)
                        finally:
                            Task.run_var.reset(token)
                except Task.Skipped:
                    pass

            return async_task_wrapper
        else:

            @wraps(func)
            @retry
            def task_wrapper(*args, **kwargs):
                try:
                    with TaskRun(self, func, args, kwargs) as run:
                        token = Task.run_var.set(run)
                        try:
                            return func(*args, **kwargs)
                        finally:
                            Task.run_var.reset(token)
                except Task.Skipped:
                    pass

            return task_wrapper


@dataclass
class TaskRun(contextlib.AbstractContextManager, contextlib.AbstractAsyncContextManager):
    config: TaskConfig
    func: Callable
    args: list[Any]
    kwargs: dict[Any, Any]

    canceled: bool = False

    @property
    def flow(self):
        return self.config.task.flow

    def cancel(self):
        self.canceled = True

    def encode_params(self):
        args = [str(x) for x in self.args]
        kwargs = [f"{k}={v}" for k, v in self.kwargs.items()]
        return ", ".join(args + kwargs)

    def __str__(self):
        return f"{self.func.__name__}({self.encode_params()})"

    def get_hash(self):
        return hashlib.md5(str(self).encode()).hexdigest()

    @cached_property
    def context(self):
        context = {}

        # hash
        if "{hash}" in self.config.location:
            context["hash"] = self.get_hash()

        # function parameters
        sig = inspect.signature(self.func)
        bound = sig.bind(*self.args, **self.kwargs)
        bound.apply_defaults()
        for key, val in bound.arguments.items():
            context[key] = val

        return context

    @cached_property
    def output_path(self):
        if self.config.location:
            return Path(self.config.location.format(**self.context))

    @cached_property
    def err_path(self):
        if path := self.output_path:
            name = path.name.removesuffix("".join(path.suffixes))
            return path.with_name(name + ".err")

    # AbstractContextManager

    def __enter__(self):
        self._stack = contextlib.ExitStack()
        self._enter_pre_contexts()

        # Limit concurrency
        if self.config.semaphore:
            self._stack.enter_context(self.config.semaphore)

        self._enter_post_contexts()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return self._stack.__exit__(exc_type, exc_val, exc_tb)

    def _enter_pre_contexts(self):
        # Task tacking
        if flow_run := self.flow.run:
            self._stack.enter_context(flow_run.track_task(self))

        # Skip the task by an exception
        if self.output_path:
            if self.output_path.exists():
                raise Task.Skipped()

            if self.err_path.exists():
                raise Task.Skipped()

    def _enter_post_contexts(self):
        # Start logging after acquiring semaphore
        self._stack.enter_context(self._logging_context())

        # Create a progress bar
        if flow_run := self.flow.run:
            if flow_progress := flow_run._progress:
                description = flow_run.TASKRUN_FORMAT.format(desc=self.encode_params())
                task_progress = TaskProgress(flow_progress, description, start=False)
                self._progress = self._stack.enter_context(task_progress)
            else:
                self._progress = None

        if self.output_path:
            self._stack.enter_context(self._delete_context(self.output_path))
            self.writer = self._stack.enter_context(self.config.compressor.writer(self.output_path))

        # Exception handling
        self._stack.enter_context(self._exception_context())

    @contextlib.contextmanager
    def _logging_context(self):
        start = time.time()
        yield
        end = time.time()
        duration = end - start

        if self.flow.verbose:
            self.flow.console.log(f"Task {self} finished in {duration:.2f}s")

    @contextlib.contextmanager
    def _delete_context(self, path):
        try:
            yield
        except BaseException:
            # Delete incomplete files on exceptions
            # Note: Catch BaseException here to handle KeyboardInterrupt, etc.
            if path.exists():
                path.unlink()
            raise

    @contextlib.contextmanager
    def _exception_context(self):
        try:
            yield
        except tuple(self.config.skip) as exc:
            self.flow.console.log(f"Task {self} skipped by {exc.__class__.__name__}")
            raise Task.Skipped() from exc
        except tuple(self.config.suppress) as exc:
            # Error log
            if self.err_path:
                with self.err_path.open("w") as f:
                    traceback.print_exception(exc, file=f)
            self.flow.console.log(f"Task {self} suppressed by {exc.__class__.__name__}")
            raise Task.Skipped() from exc

    # AbstractAsyncContextManager

    async def __aenter__(self):
        self._stack = contextlib.AsyncExitStack()
        self._enter_pre_contexts()

        # Limit concurrency
        if self.config.semaphore:
            await self._stack.enter_async_context(self.config.semaphore)

        self._enter_post_contexts()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        return await self._stack.__aexit__(exc_type, exc_val, exc_tb)
