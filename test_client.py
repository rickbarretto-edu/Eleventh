
import asyncio

from quickapi.tcp import TcpClient

async def run_demo():
    host = "127.0.0.1"
    port = 8080

    async def client_task(msg: str):
        async with TcpClient(host, port) as client:
            await client.send(msg + "\n")
            data = await client.receive()
            print("Client received:", data.rstrip())

    async with asyncio.TaskGroup() as clients:
        for i in range(4000):
            clients.create_task(client_task(f"hello {i}"))


asyncio.run(run_demo())