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


Management
~~~~~~~~~~

Attach Peer
-----------

    $ curl -X POST https://127.0.0.1:8001/cluster/attach -d '{"peer":"127.0.0.1:8002"}' -H "Content-Type: application/json"
    $ curl -X POST https://127.0.0.1:8001/cluster/attach -d '{"peer":"127.0.0.1:8003"}' -H "Content-Type: application/json"

Detach Peer
-----------

    $ curl -X POST https://127.0.0.1:8001/cluster/detach -d '{"peer":"127.0.0.1:8002"}' -H "Content-Type: application/json"

Cluster Health
--------------

    $ curl https://127.0.0.1:8001/cluster/health
    { "peers": [{"address": "127.0.0.1:8002", "status": "active"}, {"address": "127.0.0.1:8003", "status": "inactive"}] }

"""

from __future__ import annotations

from fastapi import FastAPI


app = FastAPI(
    title="Rewarding Generation Service", 
    version="0.1.0",
    debug=True,
)