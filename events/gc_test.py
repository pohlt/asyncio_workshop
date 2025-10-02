import asyncio

from hevent import HEvent


async def main():
    event = HEvent()
    ce = []
    for i in range(100):
        if i < 50:
            x = event.child
        else:
            ce.append(event.child)
    print("Child events created without memory leaks.")
    print(len(event._children))
    event.set()
    await event.wait()


if __name__ == "__main__":
    asyncio.run(main())
