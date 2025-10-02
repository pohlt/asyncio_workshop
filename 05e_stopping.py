import asyncio
import contextvars

stop = contextvars.ContextVar("stop")
stop.set(asyncio.Event())

print(stop.get())


async def do_sth(level: int):
    if level < 2:
        asyncio.create_task(do_sth(level + 1))

    for i in range(10):
        if stop.is_set():
            break
        print("I'm alive:", i)
        await asyncio.sleep(1)

    print("cleaning up")


async def main():
    asyncio.create_task(do_sth(0))
    await asyncio.sleep(3)
    stop.set()
    await asyncio.sleep(3)
    print("Main done")


asyncio.run(main())
