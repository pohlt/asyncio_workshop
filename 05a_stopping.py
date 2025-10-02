import asyncio


async def do_sth(level: int):
    if level < 2:
        asyncio.create_task(do_sth(level + 1))

    for i in range(10):
        print("I'm alive:", i)
        await asyncio.sleep(1)

    print("clean up")


async def main():
    t = asyncio.create_task(do_sth(0))
    await asyncio.sleep(3)
    t.cancel()
    await asyncio.sleep(3)
    print("Main done")


asyncio.run(main())
