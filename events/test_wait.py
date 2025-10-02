import asyncio

from hevent import EventOut, HEvent, run_while_not_event_set


async def c_old(evt: HEvent):
    async def aux(v: float):
        await asyncio.sleep(5)
        return 42 * v

    try:
        v = await run_while_not_event_set(evt, aux(5))
        print(v)
    except EventSet:
        print("event set")


async def c(evt: HEvent):
    async def aux(v: float):
        await asyncio.sleep(5)
        return 42 * v

    async with evt.TaskGroup() as tg:
        v = tg.create_task(aux(5))
        print("A", v)

    print("B", v)


async def main():
    e = HEvent()
    c_task = asyncio.create_task(c(e.child))
    await asyncio.sleep(2)
    e.set()
    await c_task


if __name__ == "__main__":
    asyncio.run(main())
