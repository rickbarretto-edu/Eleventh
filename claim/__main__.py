"""Rewarding Claiming service.

At A Glance
===========

Run this using:

    $ python -m claim --host 127.0.0.1 --port 8011
    $ python -m claim --host 127.0.0.1 --port 8012
    $ python -m claim --host 127.0.0.1 --port 8013
    

You can open the browser in the following URLs:
- http://127.0.0.1:8011: For user interface.
- http://127.0.0.1:8011/admin: For admin interface.
- http://127.0.0.1:8011/docs: For API documentation.

As Admin
~~~~~~~~

As Admin, you can attach/detach peers and check cluster health.
You can also see the log of the system and add cards as well.

As User
~~~~~~~

As User, you can claim rewards.
And this is visible for everyone in the cluster and you can check this as an admin.


Running from Shell
==================

After running the above commands, you can also interact with the service:

Service
~~~~~~~

Claim Rewards
-------------

    $ curl -X POST https://127.0.0.1:8011/api/claim?n=5
    { 
        "status": "success", 
        "cards": [ 
            { "id": 1, "name": "Card 1", "power": 15 }, 
            { "id": 2, "name": "Card 2", "power": 10 },
            { "id": 3, "name": "Card 3", "power": 20 }, 
            { "id": 4, "name": "Card 4", "power": 25 }, 
            { "id": 5, "name": "Card 5", "power": 30 } 
        ] 
    }


Management
~~~~~~~~~~

Attach Peer
-----------

    $ curl -X POST https://127.0.0.1:8011/cluster/attach -d '{"peer":"127.0.0.1:8012"}' -H "Content-Type: application/json"
    { "status": "success", "attached_peer": "127.0.0.1:8012" }
    $ curl -X POST https://127.0.0.1:8011/cluster/attach -d '{"peer":"127.0.0.1:8013"}' -H "Content-Type: application/json"
    { "status": "success", "attached_peer": "127.0.0.1:8013" }

Detach Peer
-----------

    $ curl -X POST https://127.0.0.1:8011/cluster/detach -d '{"peer":"127.0.0.1:8012"}' -H "Content-Type: application/json"
    { "status": "success", "detached_peer": "127.0.0.1:8012" }

Cluster Health
--------------

    $ curl https://127.0.0.1:8011/cluster/health
    { 
        "peers": [
            {"address": "127.0.0.1:8012", "status": "active"}, 
            {"address": "127.0.0.1:8013", "status": "inactive"}
        ]
    }

"""

from __future__ import annotations

from claim.cli import app

if __name__ == "__main__":
    app()