import asyncio


async def calc(v: int) -> int:
    await asyncio.sleep(1)
    return 42 * v


async def main():
    print(f"{calc=}")
    coro = calc(5)
    print(f"{coro=}")

    while True:
        try:
            result = coro.send(None)
        except StopIteration as e:
            result = e.value
            print(result)
            break


asyncio.run(main())
