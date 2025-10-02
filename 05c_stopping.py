import asyncio


async def do_sth(level: int):
    asyncio.current_task().add_done_callback(cleanup)  # similar to defer in Go

    if level < 2:
        asyncio.create_task(do_sth(level + 1))

    for i in range(10):
        print("I'm alive:", i)
        await asyncio.sleep(1)


def cleanup(task: asyncio.Task):
    print("Cleaning up", task)


async def main():
    t = asyncio.create_task(do_sth(0))
    # t.add_done_callback(cleanup)
    await asyncio.sleep(3)
    t.cancel()
    await asyncio.sleep(3)
    print("Main done")


asyncio.run(main())
