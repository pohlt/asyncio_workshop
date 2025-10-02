import asyncio

from hevent import HEvent

N = 5


async def child(i: int, event: HEvent) -> None:
    print(i, "started")
    if i < N:
        task = asyncio.create_task(child(i + 1, event.child))
        while not event.is_set():
            print(i, "working")
            await asyncio.sleep(0.1)
        await task
    else:
        print(i, "CRSAHING")
        raise RuntimeError("CRASHING")
    print(i, "finished")


async def main() -> None:
    print("main: started")
    event = HEvent()
    c = asyncio.create_task(child(1, event))
    await asyncio.sleep(1)
    print("main: cancelling child task")
    event.set()
    await c
    print("main: finished")


if __name__ == "__main__":
    asyncio.run(main())
    print("done")
