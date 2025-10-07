import asyncio
from collections.abc import Callable, Coroutine
from types import CoroutineType
from typing import Any

stop_event = asyncio.Event()


class WatchedTask:
    def __init__(self, restart: bool, func: Coroutine[Any, Any, Any], *args, **kwargs) -> None:
        self.restart = restart
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._task_handler_task = asyncio.create_task(self._task_handler())

    async def _task_handler(self) -> None:
        while True:
            self.task = asyncio.create_task(self.func(*self.args, **self.kwargs))
            try:
                await self.task
            except asyncio.CancelledError:
                pass
            except Exception as e:
                print(f"Task crashed with exception: {e}")
                if not self.restart:
                    raise
                await asyncio.sleep(1)
            else:
                break

    def __await__(self):
        return self.task.__await__()


class Fetcher:
    def __init__(self, size: int) -> None:
        self.size = size
        self.data = b""
        self.done = False

    async def fetch(self):
        reader, writer = await asyncio.open_connection("coherentminds.de", 32154)

        writer.write(f"{self.size}\n".encode())
        await writer.drain()

        while len(self.data) < self.size:
            self.data += await reader.read(self.size - len(self.data))

        writer.close()
        await writer.wait_closed()
        self.done = True


class FetcherManager:
    def __init__(self, n_fetchers: int, size: int) -> None:
        self.fetchers = [Fetcher(size) for _ in range(n_fetchers)]
        self.log_progress_task = WatchedTask(True, self.log_progress)

    async def fetch(self):
        async with asyncio.TaskGroup() as tg:
            for fetcher in self.fetchers:
                tg.create_task(fetcher.fetch())

        stop_event.set()
        await self.log_progress_task

    async def log_progress(self) -> int:
        while not stop_event.is_set():
            total = sum(len(f.data) for f in self.fetchers)
            print(
                f"total received: {total} bytes; "
                f"done: {sum(f.done for f in self.fetchers)}/{len(self.fetchers)}"
            )
            xxx
            await asyncio.sleep(1)

        print("I cleaned up")


async def main():
    await FetcherManager(10, 32 * 1024).fetch()


if __name__ == "__main__":
    asyncio.run(main())
    print("done")
