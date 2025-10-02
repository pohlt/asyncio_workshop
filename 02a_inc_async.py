import asyncio

val = 0


async def inc():
    global val

    if val < 10:
        print("increasing")
        await asyncio.sleep(0.1)
        val += 1


async def main():
    await asyncio.gather(*(inc() for _ in range(100)))
    print(val)


if __name__ == "__main__":
    asyncio.run(main())
