import asyncio
from cyclopts import App as CliApp
from fastapi import FastAPI
import uvicorn

from node.peers import join_peers, PEERS
from node.router import router as cluster

def plug_cluster(cli: CliApp, webserver: FastAPI):

    @cli.command()
    def start(node: str, join: str | None = None):
        """Start a node
    
        Usage
        -----
            start Node1@127.0.0.1:8000
            start Node2@127.0.0.1:8001 --join 127.0.0.1:8000
            start Node2@127.0.0.1:8002 --join 127.0.0.1:8000
        """
        loop = asyncio.get_event_loop()
        host, port = node.split("@")[1].split(":")
        join_list = [join] if join else []
    
        loop.run_until_complete(join_peers(node, join_list))    
        print(f"Node {node} started. Known peers: {PEERS}")

        webserver.include_router(cluster)
        uvicorn.run(webserver, host=host, port=int(port))
