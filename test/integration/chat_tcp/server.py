import asyncio

from quickapi.tcp import Server, Connection

Chat = Connection

clients: set[Chat] = set()

async def chat(current: Chat) -> None:
    async with current:
        clients.add(current)
        print(f"[+] {current.address} connected")
        try:
            while True:
                if not (msg := await current.receive()):
                    break
                # Broadcast to others
                for c in clients:
                    if c is not current:
                        await c.send(f"{current.address}: {msg}")
        finally:
            clients.remove(current)
            print(f"[-] {current.address} disconnected")

async def main():
    async with Server.local_at(port=5000).handles(chat) as server:
        print(f"Server running on {server.address}")
        await server.forever()

if __name__ == "__main__":
    asyncio.run(main())
