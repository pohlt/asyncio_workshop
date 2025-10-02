import asyncio

N = 5


async def child(i: int) -> None:
    print(i, "started")
    if i < N:
        task = asyncio.create_task(child(i + 1))
        while True:
            print(i, "working")
            await asyncio.sleep(0.1)
        await task
    else:
        print(i, "CRSAHING")
        raise RuntimeError("CRASHING")
    print(i, "finished")


async def main() -> None:
    print("main: started")
    print(await child(999))

    c = asyncio.create_task(child(1))
    await asyncio.sleep(1)
    print("main: cancelling child task")

    c.cancel()
    # await c
    print("main: finished")
    asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
    print("done")
