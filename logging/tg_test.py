import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

logging.basicConfig(level="INFO")
log = logging.getLogger("tg_test")


class TaskNameFilter(logging.Filter):
    def filter(self, record):
        try:
            task = asyncio.current_task()
            record.task_name = task.get_name() if task else "NoTask"
        except Exception:
            record.task_name = "NoTask"
        return True


log.addFilter(TaskNameFilter())

formatter = logging.Formatter("[%(task_name)10s] %(asctime)s %(levelname)s %(name)s: %(message)s")
for handler in logging.root.handlers:
    handler.setFormatter(formatter)


class C:
    async def bg_task(self) -> None:
        for i in range(10):
            log.info("bg task %i", i)
            await asyncio.sleep(1)

    @asynccontextmanager
    async def run(self) -> AsyncGenerator[asyncio.TaskGroup]:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.bg_task(), name="bg task")
            yield tg

    async def do_something(self) -> None:
        await asyncio.sleep(1)
        log.info("did something")


async def main() -> None:
    c = C()
    async with c.run() as tg:
        # could use the TaskGroup
        tg.create_task(c.do_something(), name="main task")
        # or not
        await c.do_something()


if __name__ == "__main__":
    asyncio.run(main())
