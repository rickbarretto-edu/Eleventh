import asyncio

from quickapi.tcp import Server, Connection

Chat = Connection

clients: set[Chat] = set()

def disconnect(chat):
    clients.remove(chat)
    print(f"[-] {chat.address} disconnected")

def connect(chat):
    clients.add(chat)
    print(f"[+] {chat.address} connected")

async def broadcast_others(self: Chat, message: str):
    for client in clients:
        if client is not self:
            await client.send(f"{self.address}: {message}")


async def chat(current: Chat) -> None:
    async with current:
        connect(current)
        try:
            while True:
                if not (msg := await current.receive()):
                    break
                await broadcast_others(current, msg)
        finally:
            disconnect(current)


async def main():
    async with Server.local_at(port=5000).handles(chat) as server:
        print(f"Server running on {server.address}")
        await server.forever()

if __name__ == "__main__":
    asyncio.run(main())
