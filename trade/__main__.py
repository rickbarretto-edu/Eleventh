"""Card Trading service.

At A Glance
===========

Run this using:

    $ python -m trade --host 127.0.0.1 --port 8031
    $ python -m trade --host 127.0.0.1 --port 8032
    $ python -m trade --host 127.0.0.1 --port 8033
    

You can open the browser in the following URLs:
- http://127.0.0.1:8031: For user interface.
- http://127.0.0.1:8031/admin: For admin interface.
- http://127.0.0.1:8031/docs: For API documentation.

As Admin
~~~~~~~~

As Admin, you can attach/detach peers and check cluster health.
You can also see the log of the system.

As User
~~~~~~~

As User, you can trade cards with other users.
Basicaly, you can propose trades and accept/reject trades.

Running from Shell
==================

After running the above commands, you can also interact with the service:

Service
~~~~~~~

List Global Trades
------------------

    $ curl https://127.0.0.1:8031/api/trades
    { "status": "success", "trades": [ { "id": 1, "name": "Card 1", "power": 15 }, { "id": 2, "name": "Card 2", "power": 10 } ] }

List My Trades
--------------

    $ curl https://127.0.0.1:8031/api/rick/trades
    { 
        "status": "success", 
        "proposals": [
            { 
                "id": 1, 
                "to": "morty",
                "wants": { "id": 2, "name": "Card 2", "power": 10 }, 
                "card": { "id": 2, "name": "Card 2", "power": 12 }, 
                "status": "pending" 
            },
            { 
                "id": 2,
                "to": "summer", 
                "wants": { "id": 3, "name": "Card 3", "power": 21 }, 
                "card": { "id": 3, "name": "Card 3", "power": 20 }, 
                "status": "accepted" 
            }
        ],
        "received": [
            { 
                "id": 3, 
                "from": "beth",
                "wants": { "id": 4, "name": "Card 4", "power": 26 }, 
                "card": { "id": 4, "name": "Card 4", "power": 25 }, 
                "status": "pending" 
            }
        ],
    }

Submit a Trade
----------------

    $ curl -X POST https://127.0.0.1:8031/api/rick/trade -d "{ 'id': 1, 'name': 'Card 1', 'power': 15 }"
    { "status": "success", "message": "Trade submitted" }

Propose a Trade
----------------

    $ curl -X POST https://127.0.0.1:8031/api/rick/trade/propose?to=morty&card_id=2
    { "status": "success", "message": "Trade proposed to morty" }

Accept a Trade
--------------

    $ curl -X POST https://127.0.0.1:8031/api/rick/trade/accept?id=1
    { "status": "success", "message": "Trade accepted" }

Reject a Trade
--------------

    $ curl -X POST https://127.0.0.1:8031/api/rick/trade/reject?id=1
    { "status": "success", "message": "Trade rejected" }


Management
~~~~~~~~~~

Attach Peer
-----------

    $ curl -X POST https://127.0.0.1:8031/cluster/attach -d '{"peer":"127.0.0.1:8032"}' -H "Content-Type: application/json"
    { "status": "success", "attached_peer": "127.0.0.1:8032" }
    $ curl -X POST https://127.0.0.1:8031/cluster/attach -d '{"peer":"127.0.0.1:8033"}' -H "Content-Type: application/json"
    { "status": "success", "attached_peer": "127.0.0.1:8033" }
    
Detach Peer
-----------

    $ curl -X POST https://127.0.0.1:8031/cluster/detach -d '{"peer":"127.0.0.1:8032"}' -H "Content-Type: application/json"
    { "status": "success", "detached_peer": "127.0.0.1:8032" }
    
Cluster Health
--------------

    $ curl https://127.0.0.1:8031/cluster/health
    { 
        "peers": [
            {"address": "127.0.0.1:8032", "status": "active"}, 
            {"address": "127.0.0.1:8033", "status": "inactive"}
        ]
    }

"""

from __future__ import annotations

from trade.cli import app


if __name__ == "__main__":
    app()
