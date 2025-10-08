# Clusters Package

Clustering utilities for distributed FastAPI applications.

## Usage

```python
from fastapi import FastAPI
from eleventh.clusters import ConsulPlugin

app = FastAPI()

# Attach clustering plugin
plugin = ConsulPlugin(
    nodes=[
        "http://127.0.0.1:8001",
        "http://127.0.0.1:8002",
        "http://127.0.0.1:8003",
    ],
    health_check_interval=10.0,
)
plugin.attach(app, node_address="http://127.0.0.1:8001")
```

## Features

- Background peer health monitoring
- Admin UI at `/cluster/admin`
- REST API endpoints at `/cluster/*`
- Dynamic peer management
- Configurable health check intervals
- Auto-detection of peers based on nodes list

## Endpoints

- `GET /cluster/health` - Node health check
- `GET /cluster/status` - Cluster status
- `GET /cluster/peers` - List peers
- `POST /cluster/peers/add` - Add peer
- `DELETE /cluster/peers/remove` - Remove peer
- `GET /cluster/admin` - Admin dashboard

## Configuration

```python
ConsulPlugin(
    nodes: list[str],                       # Required: all node addresses in cluster
    health_check_interval: float = 10.0,    # Check interval in seconds
    health_check_timeout: float = 5.0,      # Request timeout
)
```

The plugin automatically determines which node it is when you call `attach(app, node_address)`.
Peers are automatically set to all other nodes in the cluster.
