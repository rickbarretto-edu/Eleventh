
import asyncio

from quickapi.tcp import Server

async def run_demo():
    async with Server("127.0.0.1", 8080) as server:
        print(f"Server listening on {server.address}")
        await server.forever()

asyncio.run(run_demo())