import asyncio
from contextlib import suppress

N = 5


async def child(i: int) -> None:
    print(i, "started")
    if i < N:
        task = asyncio.create_task(child(i + 1))
        print(i, "sleeping")
        await asyncio.sleep(0.5 if i >= 3 else 3.0)
        print(i, "waking up")
        task.cancel()
        print(i, "cancelled child task")
        with suppress(asyncio.CancelledError):
            await task
        # print("RESULT", task.result())
    else:
        print("xxx")
        # xxx
    # await asyncio.Future()
    print(i, "finished")


async def main() -> None:
    print("Main started")
    c = asyncio.create_task(child(1))
    await asyncio.sleep(1)
    print("Main cancelling child task")
    c.cancel()
    with suppress(asyncio.CancelledError):
        await c
    print("Main finished")


if __name__ == "__main__":
    asyncio.run(main())
    print("done")
