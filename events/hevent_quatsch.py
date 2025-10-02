import asyncio


class HEvent(asyncio.Event):
    def __init__(self):
        super().__init__()
        self._child = None

    @property
    def child(self):
        if self._child is None:
            self._child = HEvent()
        return self._child

    def set(self):
        if self._child:
            self._child.set()
        super().set()

    def clear(self):
        if self._child:
            self.child.clear()
        super().clear()

    async def wait(self):
        if self._child:
            await self.child.wait()
        await super().wait()


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
