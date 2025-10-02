import asyncio


async def func(i: int):
    await asyncio.sleep(1)
    print("func", i)


async def main():
    tasks = [asyncio.create_task(func(i), name=f"func{i}") for i in range(5)]

    for t in asyncio.all_tasks():
        print("\t", t)
    print(asyncio.tasks._scheduled_tasks)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
