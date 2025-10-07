import asyncio


def log(msg, level):
    print(f"{'    ' * level}{level}: {msg}")


async def func(level):
    log("start", level)
    if level <= 2:
        task = asyncio.create_task(func(level + 1))
        log(f"task for level {level + 1} created", level)
        await task
        assert task.result() == 42 * (level + 1)
    log("end", level)
    return 42 * level


async def main():
    await func(0)


asyncio.run(main())
