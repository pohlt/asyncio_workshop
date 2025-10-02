import asyncio


async def handle_client(reader, writer):
    size = int((await reader.readuntil(b"\n")).decode().strip())
    writer.write(b"#" * size)
    await writer.drain()
    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 32154)
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
