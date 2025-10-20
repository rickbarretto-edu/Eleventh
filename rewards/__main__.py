"""Rewarding Generation service.

At A Glance
===========

Run this using:

    $ python -m rewards --host 127.0.0.1 --port 8001
    $ python -m rewards --host 127.0.0.1 --port 8002
    $ python -m rewards --host 127.0.0.1 --port 8003


Open https://127.0.0.1:8001/admin on Browser and connect to other peers.
Then, open https://127.0.0.1:8001 and click "Generate" button to generate text and get rewards from other peers.


Running from Shell
==================

After running the above commands, you can also interact with the service:

Service
~~~~~~~~~~

Generate 500 Cards
------------------

    $ curl -X POST https://127.0.0.1:8001/api/create?n=500

"""

from cyclopts import App as Cyclopts
from fastapi import FastAPI

from node.plugin import plug_cluster
from rewards.service.api import service
from rewards.service.web import pages

webapp = FastAPI(
    title="Rewarding Generation Service", 
    version="0.1.0",
    debug=True,
)
cli = Cyclopts(
    "rewards", 
    help="Rewarding Generation Service."
)

webapp.include_router(service)
webapp.include_router(pages)
plug_cluster(cli, webapp)

if __name__ == "__main__":
    cli()
