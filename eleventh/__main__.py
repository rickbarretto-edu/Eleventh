import asyncio
from quickapi import QuickAPI

from eleventh.login import routes as login


async def run():
    routes = login
    app = QuickAPI()

    await app.serve(routes)


def main():
    try:
        asyncio.run(run())
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()