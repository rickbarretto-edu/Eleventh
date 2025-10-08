"""Cluster management for Deck service.

This module provides CLI functionality to start multiple deck service instances
in a cluster configuration using Cyclopts.

Usage:
    python -m eleventh.decks.cluster start --addresses http://127.0.0.1:8001 http://127.0.0.1:8002 http://127.0.0.1:8003
    python -m eleventh.decks.cluster start --addresses http://127.0.0.1:8001,http://127.0.0.1:8002,http://127.0.0.1:8003
"""

import asyncio
from typing import Annotated
import uvicorn
from cyclopts import App, Parameter

from eleventh.decks.app import app as fastapi_app


cli = App(
    name="cluster",
    help="Manage deck service cluster instances",
)

def extract_host_port(address: str) -> tuple[str, int]:
    """Extract host and port from an address URL.
        
    Examples
    --------
        >>> extract_host_port("http://127.0.0.1:8001")
        ('127.0.0.1', 8001)
    """
    addr = address.replace('http://', '').replace('https://', '')
    
    if ':' not in addr:
        raise ValueError(f"Invalid address format: {address}. Expected http://host:port")
    
    host, port_str = addr.rsplit(':', 1)
    
    try:
        port = int(port_str)
    except ValueError:
        raise ValueError(f"Invalid port in address: {address}")
    
    return host, port


async def run_server(host: str, port: int, address: str, all_addresses: list[str]):
    """Run a single uvicorn server instance.
    
    Parameters
    ----------
    host: Host to bind to
    port: Port to bind to
    address: Full address URL for cluster identification
    all_addresses: All addresses in the cluster for peer configuration
    """
    # Create a new FastAPI app instance for this server
    # This ensures each server has its own state
    from eleventh.decks.app import create_app
    
    # Create app with cluster plugin
    app = create_app(node_address=address, nodes=all_addresses)
    
    config = uvicorn.Config(
        app=app,
        host=host,
        port=port,
        log_level="info",
    )
    server = uvicorn.Server(config)
    
    await server.serve()


async def start_cluster(addresses: list[str]):
    """Start multiple deck service instances as a cluster.
    
    Parameters
    ----------
    addresses: List of addresses to start servers on

    """
    tasks = []
    
    for address in addresses:
        host, port = extract_host_port(address)
        print(f"Starting deck service on {address}...")
        
        task = asyncio.create_task(run_server(host, port, address, addresses))
        tasks.append(task)
    
    try:
        await asyncio.gather(*tasks)
    except KeyboardInterrupt:
        print("\nShutting down cluster...")
        for task in tasks:
            task.cancel()
        
        await asyncio.gather(*tasks, return_exceptions=True)
        print("Cluster stopped.")


@cli.command
def start(
    addresses: Annotated[
        list[str],
        Parameter(
            help="Addresses to start deck service instances on. "
            "Format: http://host:port. Can be specified multiple times or as comma-separated values.",
        ),
    ],
):
    """Start a cluster of deck service instances.
    
    Examples
    --------

        # Start 3 instances
        cluster start --addresses http://127.0.0.1:8001 http://127.0.0.1:8002 http://127.0.0.1:8003
    """
    if not addresses:
        print("Error: At least one address must be provided")
        return 1

    print(f"Starting deck service cluster with {len(addresses)} instance(s)...")
    for addr in addresses:
        print(f"  - {addr}")
    print()
    
    try:
        asyncio.run(start_cluster(addresses))
    except KeyboardInterrupt:
        print("\nCluster stopped by user.")

    return 0


@cli.command
def version():
    """Show version information."""
    print("Deck Service Cluster Manager v0.1.0")
    return 0


def main():
    """Entry point for the cluster CLI."""
    cli()


if __name__ == "__main__":
    main()
