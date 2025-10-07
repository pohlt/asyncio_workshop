import abc
import asyncio
import logging
from asyncio import Task
from dataclasses import dataclass
from typing import Awaitable, Optional, Sequence

log = logging.getLogger("ch")


class BlockingTask(abc.ABC):
    @abc.abstractmethod
    async def blocking_start(self) -> None:
        pass

    @abc.abstractmethod
    async def shutdown(self) -> None:
        pass


@dataclass
class InterruptibleTask(BlockingTask):
    coroutine: Awaitable[None]
    name: str
    _task: Optional[Task] = None

    @property
    def is_running(self) -> bool:
        return self._task is not None and not self._task.done()

    async def blocking_start(self) -> None:
        log.info(f"Starting {self.name} task...")
        self._task = asyncio.create_task(self._main())  # TODO: > 3.7 name=self.name)
        try:
            await self._task
        except asyncio.CancelledError:
            # we need to ensure that we only consume the CanelledError if the task we are waiting
            # for was actually cancelled. If an outer task was requested to be cancelled we must
            # propagate the exception
            # https://superfastpython.com/asyncio-task-cancellation-best-practices/
            task = asyncio.current_task()
            if task is not None and task.cancelling() > 0:
                raise

    async def shutdown(self) -> None:
        if self._task is not None:
            self._task.cancel()

    async def _main(self) -> None:
        try:
            await self.coroutine
        finally:
            if self._task is not None and self._task.done():
                log.info(f"Task {self.name} was shut down")


class Sentinel(BlockingTask):
    def __init__(self) -> None:
        self._shutdown_event = asyncio.Event()

    async def blocking_start(self) -> None:
        self._shutdown_event.clear()
        await self._shutdown_event.wait()

    async def shutdown(self) -> None:
        self._shutdown_event.set()


class TaskSetManager(BlockingTask):
    def __init__(self, tasks: Sequence[BlockingTask], name: str) -> None:
        self._tasks = tasks
        self._name = name
        self._running: bool = True
        self._sentinel = Sentinel()  # make sure blocking_start blocks even on empty task lists

    async def blocking_start(self, **kwargs) -> None:
        log.info(f"Starting task set {self._name} ...")
        self._running = True
        while self._running:
            coroutines = [task.blocking_start(**kwargs) for task in self._tasks]
            coroutines_with_sentinel = coroutines + [self._sentinel.blocking_start()]
            await asyncio.gather(*coroutines_with_sentinel)
        log.info(f"Task set {self._name} successfully shutdown.")

    async def shutdown(self) -> None:
        self._running = False
        await asyncio.gather(*self._get_shutdown_coroutines())

    async def update_coroutines_deferring_start(self, tasks: Sequence[BlockingTask]) -> None:
        shutdown_coroutines = self._get_shutdown_coroutines()
        self._tasks = tasks
        await asyncio.gather(*shutdown_coroutines)
        log.info(f"Interrupted and updated task set {self._name} ...")

    def _get_shutdown_coroutines(self) -> Sequence[Awaitable]:
        return [task.shutdown() for task in self._tasks] + [self._sentinel.shutdown()]
