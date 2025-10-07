import asyncio
import time


def calc():
    time.sleep(1)


async def long_task():
    print("long task started")
    for _ in range(10):
        calc()


async def nice_long_task():
    print("nice long task started")
    for i in range(10):
        calc()
        await asyncio.sleep(0)


async def background_task():
    while True:
        print("background task is running...")
        await asyncio.sleep(1)


async def main():
    bg_task = asyncio.create_task(background_task())
    # await long_task()
    await nice_long_task()


asyncio.run(main())
