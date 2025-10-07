import asyncio
from collections.abc import Coroutine
from contextlib import asynccontextmanager, suppress
from weakref import WeakSet

asyncio.wait_for


class HEvent(asyncio.Event):
    def __init__(self):
        super().__init__()
        self._children: WeakSet[asyncio.Event] = WeakSet()

    @property
    def child(self):
        new_child = HEvent()
        self._children.add(new_child)
        return new_child

    def set(self):
        for child in self._children:
            child.set()
        super().set()

    def clear(self):
        for child in self._children:
            child.clear()
        super().clear()

    async def wait(self):
        for child in self._children:
            await child.wait()
        await super().wait()

    async def event_out(self, tg: asyncio.TaskGroup):
        tg._on_task_done
        t = tg.create_task(self.wait())
        t.add_done_callback()

    async def TaskGroup(self):
        tg = asyncio.TaskGroup()

        @asynccontextmanager
        async def aux():
            async with tg:
                yield tg

        # tg_task = asyncio.create_task(aux())
        # event_task = asyncio.create_task(self.wait())
        return aux()


class EventOut(Exception): ...


async def run_while_not_event_set(event: HEvent, coro: Coroutine):
    event_task = asyncio.create_task(event.wait())
    coro_task = asyncio.create_task(coro)
    _, pending = await asyncio.wait((event_task, coro_task), return_when=asyncio.FIRST_COMPLETED)

    for t in pending:
        t.cancel()
        with suppress(asyncio.CancelledError):
            await t

    if not coro_task.cancelled():
        assert coro_task.done()
        return coro_task.result()
    else:
        assert event.is_set() and event_task.done()
        raise EventOut()


async def main():
    event = HEvent()
    child_event = event.child

    async def child():
        print("Child task waiting for event")
        await child_event.wait()
        print("Child task finished")

    child_task = asyncio.create_task(child())

    print("Main task sleeping for 2 seconds")
    await asyncio.sleep(2)
    print("Main task setting event")
    event.set()

    await child_task


if __name__ == "__main__":
    asyncio.run(main())
