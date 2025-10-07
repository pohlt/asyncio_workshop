import asyncio
import sys
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from loguru import logger


def get_task_name() -> str:
    try:
        task = asyncio.current_task()
        return task.get_name() if task else "NoName"
    except Exception:
        return "NoTask"


logger.configure(patcher=lambda record: record["extra"].update(task_name=get_task_name()))
logger.remove(0)
# adapted from loguru._default.LOGURU_FORMAT
format = "<green>{time:HH:mm:ss.SS}</green> | <level>{level: <8}</level> | <cyan>{extra[task_name]}</cyan> | <level>{message}</level>"
logger.add(sys.stderr, format=format, level="INFO")


class C:
    async def bg_task(self) -> None:
        for i in range(10):
            logger.info("bg task {}", i)
            await asyncio.sleep(1)

    @asynccontextmanager
    async def run(self) -> AsyncGenerator[asyncio.TaskGroup]:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(self.bg_task(), name="bg task")
            yield tg

    async def do_something(self) -> None:
        await asyncio.sleep(1)
        logger.info("did something")


async def main() -> None:
    c = C()
    async with c.run() as tg:
        # could use the TaskGroup
        tg.create_task(c.do_something(), name="main task")
        # or not
        await c.do_something()


if __name__ == "__main__":
    asyncio.run(main())
