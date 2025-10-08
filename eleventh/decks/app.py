"""Deck management microservice.

Usage
-----

        uvicorn eleventh.decks.app:app --reload --host --port 8000
"""


from typing import Optional
from fastapi import FastAPI

from eleventh.decks.web import api
from eleventh.decks.web import pages
from eleventh.clusters import ConsulPlugin


def create_app(
    node_address: Optional[str] = None,
    nodes: Optional[list[str]] = None,
    enable_clustering: bool = True,
) -> FastAPI:
    """Create and configure a FastAPI application.
    
    Parameters
    ----------
    node_address : str, optional
        The address of this node for clustering
    nodes : list[str], optional
        List of all node addresses in the cluster (including this one)
    enable_clustering : bool
        Whether to enable the clustering plugin
    
    Returns
    -------
    FastAPI
        Configured FastAPI application
    """
    app = FastAPI(title="Deck Management Service")
    app.include_router(pages.route)
    app.include_router(api.route)
    
    # Add clustering plugin if enabled and configured
    if enable_clustering and node_address and nodes:
        plugin = ConsulPlugin(
            nodes=nodes,
            health_check_interval=10.0,
        )
        plugin.attach(app, node_address=node_address)
    
    return app


# Default app instance for standalone usage
app = create_app(enable_clustering=False)

