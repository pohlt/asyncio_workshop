import asyncio
import threading
import time


async def calc_async(x):
    print("calc_async started")
    time.sleep(1)
    return 42 * x


def calc_sync(x):
    print("calc_sync started")
    time.sleep(1)
    return 42 * x


async def main_single_thread():
    tasks = [asyncio.create_task(calc_async(i)) for i in range(5)]
    results = await asyncio.gather(*tasks)
    print(results)


async def main_multi_thread():
    coros = [asyncio.to_thread(calc_sync, i) for i in range(5)]
    print("create coros, but not yet tasks")  # threads not yet started
    tasks = [asyncio.create_task(coro) for coro in coros]
    await asyncio.sleep(0.5)  # give threads time to start
    print(threading.active_count())
    results = await asyncio.gather(*tasks)
    print(results)


# asyncio.run(main_single_thread())
asyncio.run(main_multi_thread())
