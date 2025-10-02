import asyncio
import gc
import time


async def calc() -> None:
    for i in range(10_000):
        if i & 31 == 0:
            print("calculating", i)
        time.sleep(0.1)
        await asyncio.sleep(0)


async def main():
    t = asyncio.create_task(calc())

    for _ in range(10):
        print(gc.get_referrers(t))
        gc.collect()
        await asyncio.sleep(3)


asyncio.run(main())
print("done")
