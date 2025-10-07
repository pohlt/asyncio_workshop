import asyncio
import time


def log(msg):
    print(f"{time.monotonic():.2f} {msg}")


async def bg():
    while True:
        log("bg task")
        await asyncio.sleep(1)


def busy_sleep(delay):
    start_time = time.monotonic()
    while time.monotonic() - start_time < delay:
        pass


async def sleep():
    while True:
        log("busy_sleep")
        busy_sleep(1)
        # time.sleep(1)
        await asyncio.sleep(0)


async def main():
    bg_task = asyncio.create_task(bg())
    await asyncio.sleep(0.5)
    sleep_task = asyncio.create_task(sleep())
    await asyncio.Future()


asyncio.run(main())
