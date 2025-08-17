import asyncio

from quickapi.tcp import Client

async def listen(client: Client):
    while (message := await client.receive()):
        print(message)

async def talk(client: Client):
    loop = asyncio.get_event_loop()
    while True:
        msg = await loop.run_in_executor(None, input, "")
        await client.send(msg)

async def main():
    async with Client.to_localhost(at=5000) as client:
        print("Connected to chat server.")
        await asyncio.gather(
            listen(client),
            talk(client),
        )

if __name__ == "__main__":
    asyncio.run(main())
