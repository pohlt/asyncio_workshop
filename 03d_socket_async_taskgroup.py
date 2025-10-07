import asyncio


async def fetch(size: int):
    reader, writer = await asyncio.open_connection("coherentminds.de", 32154)

    writer.write(f"{size}\n".encode())
    await writer.drain()

    data = b""
    while len(data) < size:
        data += await reader.read(size - len(data))

    writer.close()
    await writer.wait_closed()
    print(f"received {len(data)} bytes")


async def main():
    async with asyncio.TaskGroup() as tg:
        for _ in range(10):
            tg.create_task(fetch(32 * 1024))


if __name__ == "__main__":
    asyncio.run(main())
