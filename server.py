import asyncio
from random import randint, random


async def handle_client(reader, writer):
    size = min(1024**2, int((await reader.readuntil(b"\n")).decode().strip()))
    await asyncio.sleep(0.1 + random())
    sent = 0
    while sent < size:
        sending = min(randint(512, 2048), size - sent)
        writer.write(b"#" * sending)
        await writer.drain()
        sent += sending
        await asyncio.sleep(0.5 * random())

    writer.close()
    await writer.wait_closed()


async def main():
    server = await asyncio.start_server(handle_client, "0.0.0.0", 32154)
    await server.serve_forever()


if __name__ == "__main__":
    asyncio.run(main())
