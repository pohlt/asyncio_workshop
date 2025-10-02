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
    tasks = [fetch(1024 * 1024) for _ in range(10)]
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
