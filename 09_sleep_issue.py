import asyncio
import time

start_time = time.monotonic()


def log(msg):
    print(f"{time.monotonic() - start_time:.2f} {msg}")


async def bg_task():
    while True:
        log("bg")
        await asyncio.sleep(1)


async def fg_task():
    while True:
        log("fg -----------")
        # long computation
        time.sleep(1)
        await asyncio.sleep(0)
        await asyncio.sleep(0)
        await asyncio.sleep(0)


async def main():
    asyncio.create_task(bg_task())
    await asyncio.sleep(0.5)
    asyncio.create_task(fg_task())
    await asyncio.Future()


asyncio.run(main())
