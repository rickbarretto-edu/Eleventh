import asyncio

from quickapi.tcp import Server, Connection

clients: set[Connection] = set()

async def chat(conn: Connection) -> None:
    async with conn:
        clients.add(conn)
        print(f"[+] {conn.address} connected")
        try:
            while True:
                if not (msg := await conn.receive()):
                    break
                # Broadcast to others
                for c in clients:
                    if c is not conn:
                        await c.send(f"{conn.address}: {msg}")
        finally:
            clients.remove(conn)
            print(f"[-] {conn.address} disconnected")

async def main():
    async with Server(host="127.0.0.1", port=5000, handles=chat) as server:
        print(f"Server running on {server.address}")
        await server.forever()

if __name__ == "__main__":
    asyncio.run(main())
