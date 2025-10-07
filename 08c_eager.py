import asyncio
from time import perf_counter


def log(msg, level):
    # print(f"{'    ' * level}{level}: {msg}")
    pass


async def func(level):
    # await asyncio.sleep(0)
    log("start", level)
    if level <= 10:
        for _ in range(3):
            task = asyncio.create_task(func(level + 1))
            log(f"task for level {level + 1} created", level)
            await task
            assert task.result() == 42 * (level + 1)
    log("end", level)
    return 42 * level


async def main():
    asyncio.get_running_loop().set_task_factory(asyncio.eager_task_factory)
    start_time = perf_counter()
    await func(0)
    print(f"completed in {perf_counter() - start_time:.2f} seconds")


asyncio.run(main())
