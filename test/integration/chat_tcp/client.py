import asyncio

import attrs

from quickapi.tcp import Client

@attrs.define
class Chat:
    client: Client

    async def listen(self) -> None:
        while (message := await self.client.receive()):
            print(message)

    async def talk(self):
        loop = asyncio.get_event_loop()
        while True:
            message = await loop.run_in_executor(None, input, "")
            await self.client.send(message)


async def open_chat_group():
    async with Client.to_localhost(at=5000) as client:
        print("Connected to chat server.")
        chat = Chat(client)
        await asyncio.gather(
            chat.listen(),
            chat.talk(),
        )

if __name__ == "__main__":
    asyncio.run(open_chat_group())
