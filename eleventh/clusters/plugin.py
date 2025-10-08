"""Consul-like clustering plugin for FastAPI applications.

This module provides a plugin that adds clustering capabilities to FastAPI applications,
including peer health checking, service discovery, and an admin interface.

Features:
- Automatic peer health checking with configurable intervals
- HTTP endpoints for cluster management (/cluster/*)
- Admin web UI to monitor peer health (/cluster/admin)
- Background health check tasks
- Peer registration and deregistration

Usage:
    from eleventh.clusters import ConsulPlugin
    
    app = FastAPI()
    plugin = ConsulPlugin(
        nodes=[
            "http://127.0.0.1:8001",
            "http://127.0.0.1:8002",
            "http://127.0.0.1:8003",
        ],
        health_check_interval=10.0
    )
    plugin.attach(app)
    
    # The plugin will automatically determine which node it is
    # when the server starts based on the host:port
"""

import asyncio
import time
from datetime import datetime
from pathlib import Path
from typing import Literal
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, APIRouter
from fastapi.responses import HTMLResponse
from pydantic import BaseModel


class PeerStatus(BaseModel):
    """Status information for a peer node."""
    address: str
    status: Literal["healthy", "unhealthy", "unknown"]
    last_check: float | None = None
    last_success: float | None = None
    response_time_ms: float | None = None
    error: str | None = None


class ClusterInfo(BaseModel):
    """Information about the current cluster state."""
    node_address: str
    peers: list[PeerStatus]
    cluster_size: int
    healthy_peers: int
    last_updated: float


class HealthCheckResponse(BaseModel):
    """Response from a health check endpoint."""
    status: str
    node_address: str
    timestamp: float
    version: str = "0.1.0"


class ConsulPlugin:
    """Consul-like clustering plugin for FastAPI applications.
    
    This plugin adds clustering capabilities to FastAPI apps including:
    - Peer health monitoring
    - Service discovery endpoints
    - Admin UI for cluster monitoring
    
    Attributes
    ----------
    nodes : list[str]
        List of all nodes in the cluster (including this one)
    node_address : str
        The address of this node (auto-detected)
    peers : list[str]
        List of peer node addresses to monitor (nodes minus this one)
    health_check_interval : float
        Seconds between health checks (default: 10.0)
    """
    
    def __init__(
        self,
        nodes: list[str],
        health_check_interval: float = 10.0,
        health_check_timeout: float = 5.0,
    ):
        """Initialize the Consul plugin.
        
        Parameters
        ----------
        nodes : list[str]
            List of all node addresses in the cluster (including this one).
            The plugin will auto-detect which node it is based on server host:port.
        health_check_interval : float
            Seconds between health checks
        health_check_timeout : float
            Timeout for health check requests in seconds
        """
        self.nodes = nodes
        self.node_address: str | None = None  # Will be set in attach()
        self.peers: list[str] = []  # Will be set in attach()
        self.health_check_interval = health_check_interval
        self.health_check_timeout = health_check_timeout
        
        # Store peer status
        self._peer_status: dict[str, PeerStatus] = {}
        self._health_check_task: asyncio.Task | None = None
        self._shutdown_event = asyncio.Event()
    
    def attach(self, app: FastAPI, node_address: str) -> None:
        """Attach the plugin to a FastAPI application.
        
        This adds cluster management endpoints and starts background health checks.
        
        Parameters
        ----------
        app : FastAPI
            The FastAPI application to attach to
        node_address : str
            The address of this node (e.g., "http://127.0.0.1:8001").
            Must be one of the addresses in the nodes list.
        """
        # Validate and set node address
        if node_address not in self.nodes:
            raise ValueError(
                f"node_address '{node_address}' must be in the nodes list: {self.nodes}"
            )
        
        self.node_address = node_address
        
        # Set peers (all nodes except this one)
        self.peers = [node for node in self.nodes if node != self.node_address]
        
        # Initialize peer status
        for peer in self.peers:
            self._peer_status[peer] = PeerStatus(
                address=peer,
                status="unknown",
            )
        
        # Store reference to app
        self.app = app
        
        # Create router for cluster endpoints
        router = self._create_router()
        app.include_router(router)
        
        # Add lifespan event handlers using the new lifespan pattern
        original_lifespan = app.router.lifespan_context
        
        @asynccontextmanager
        async def lifespan_with_plugin(app: FastAPI):
            # Startup
            await self._startup()
            
            # If there was an original lifespan, call it
            if original_lifespan:
                async with original_lifespan(app):
                    yield
            else:
                yield
            
            # Shutdown
            await self._shutdown()
        
        app.router.lifespan_context = lifespan_with_plugin
    
    def _create_router(self) -> APIRouter:
        """Create the router with cluster management endpoints."""
        router = APIRouter(prefix="/cluster", tags=["cluster"])
        
        @router.get("/health")
        async def health_check():
            """Health check endpoint for this node."""
            assert self.node_address is not None, "Plugin not attached to app"
            return HealthCheckResponse(
                status="healthy",
                node_address=self.node_address,
                timestamp=time.time(),
            )
        
        @router.get("/status")
        async def cluster_status() -> ClusterInfo:
            """Get the current cluster status."""
            assert self.node_address is not None, "Plugin not attached to app"
            healthy_count = sum(
                1 for status in self._peer_status.values() 
                if status.status == "healthy"
            )
            
            return ClusterInfo(
                node_address=self.node_address,
                peers=list(self._peer_status.values()),
                cluster_size=len(self.peers) + 1,  # +1 for this node
                healthy_peers=healthy_count,
                last_updated=time.time(),
            )
        
        @router.get("/peers")
        async def list_peers():
            """List all known peer addresses."""
            assert self.node_address is not None, "Plugin not attached to app"
            return {
                "node_address": self.node_address,
                "node_address": self.node_address,
                "peers": self.peers,
                "total_peers": len(self.peers),
            }
        
        @router.post("/peers/add")
        async def add_peer(peer_address: str):
            """Add a new peer to the cluster."""
            if peer_address not in self.peers:
                self.peers.append(peer_address)
                self._peer_status[peer_address] = PeerStatus(
                    address=peer_address,
                    status="unknown",
                )
                return {"message": f"Peer {peer_address} added", "success": True}
            return {"message": f"Peer {peer_address} already exists", "success": False}
        
        @router.delete("/peers/remove")
        async def remove_peer(peer_address: str):
            """Remove a peer from the cluster."""
            if peer_address in self.peers:
                self.peers.remove(peer_address)
                self._peer_status.pop(peer_address, None)
                return {"message": f"Peer {peer_address} removed", "success": True}
            return {"message": f"Peer {peer_address} not found", "success": False}
        
        @router.get("/admin", response_class=HTMLResponse)
        async def admin_page():
            """Admin UI to monitor cluster health."""
            return self._render_admin_page()
        
        return router
    
    async def _startup(self):
        """Start background health check task."""
        print(f"[Consul Plugin] Starting cluster monitoring for node {self.node_address}")
        print(f"[Consul Plugin] Monitoring {len(self.peers)} peer(s)")
        
        # Start health check task
        self._health_check_task = asyncio.create_task(self._health_check_loop())
    
    async def _shutdown(self):
        """Stop background health check task."""
        print("[Consul Plugin] Shutting down cluster monitoring")
        
        # Signal shutdown
        self._shutdown_event.set()
        
        # Cancel health check task
        if self._health_check_task:
            self._health_check_task.cancel()
            try:
                await self._health_check_task
            except asyncio.CancelledError:
                pass
    
    async def _health_check_loop(self):
        """Background task that periodically checks peer health."""
        while not self._shutdown_event.is_set():
            try:
                await self._check_all_peers()
            except Exception as e:
                print(f"[Consul Plugin] Error in health check loop: {e}")
            
            # Wait for next interval
            try:
                await asyncio.wait_for(
                    self._shutdown_event.wait(),
                    timeout=self.health_check_interval
                )
            except asyncio.TimeoutError:
                continue
    
    async def _check_all_peers(self):
        """Check health of all peers."""
        async with httpx.AsyncClient(timeout=self.health_check_timeout) as client:
            tasks = [
                self._check_peer_health(client, peer)
                for peer in self.peers
            ]
            await asyncio.gather(*tasks, return_exceptions=True)
    
    async def _check_peer_health(self, client: httpx.AsyncClient, peer_address: str):
        """Check health of a single peer.
        
        Parameters
        ----------
        client : httpx.AsyncClient
            HTTP client to use for the request
        peer_address : str
            Address of the peer to check
        """
        start_time = time.time()
        
        try:
            response = await client.get(f"{peer_address}/cluster/health")
            response_time_ms = (time.time() - start_time) * 1000
            
            if response.status_code == 200:
                self._peer_status[peer_address] = PeerStatus(
                    address=peer_address,
                    status="healthy",
                    last_check=time.time(),
                    last_success=time.time(),
                    response_time_ms=response_time_ms,
                    error=None,
                )
            else:
                self._peer_status[peer_address] = PeerStatus(
                    address=peer_address,
                    status="unhealthy",
                    last_check=time.time(),
                    response_time_ms=response_time_ms,
                    error=f"HTTP {response.status_code}",
                )
        
        except Exception as e:
            self._peer_status[peer_address] = PeerStatus(
                address=peer_address,
                status="unhealthy",
                last_check=time.time(),
                response_time_ms=None,
                error=str(e),
            )
    
    def _render_admin_page(self) -> str:
        """Render the admin UI page."""
        assert self.node_address is not None, "Plugin not attached to app"
        
        # Load the HTML template
        template_path = Path(__file__).parent / "static" / "admin.html"
        with open(template_path, "r", encoding="utf-8") as f:
            template = f.read()
        
        # Calculate cluster statistics
        total_peers = len(self.peers)
        healthy_peers = sum(
            1 for status in self._peer_status.values() 
            if status.status == "healthy"
        )
        unhealthy_peers = sum(
            1 for status in self._peer_status.values() 
            if status.status == "unhealthy"
        )
        unknown_peers = total_peers - healthy_peers - unhealthy_peers
        
        # Build peer rows HTML
        peer_rows = []
        for peer_addr in sorted(self.peers):
            status = self._peer_status.get(peer_addr)
            if not status:
                continue
            
            status_badge_class = {
                "healthy": "success",
                "unhealthy": "danger",
                "unknown": "secondary",
            }.get(status.status, "secondary")
            
            last_check_str = (
                datetime.fromtimestamp(status.last_check).strftime("%Y-%m-%d %H:%M:%S")
                if status.last_check else "Never"
            )
            
            response_time_str = (
                f"{status.response_time_ms:.2f} ms"
                if status.response_time_ms is not None else "N/A"
            )
            
            error_str = status.error if status.error else "—"
            
            peer_rows.append(f"""
                <tr>
                    <td>{status.address}</td>
                    <td><span class="badge bg-{status_badge_class}">{status.status.upper()}</span></td>
                    <td>{last_check_str}</td>
                    <td>{response_time_str}</td>
                    <td class="text-danger">{error_str}</td>
                </tr>
            """)
        
        peer_table = "\n".join(peer_rows) if peer_rows else '<tr><td colspan="5" class="text-center text-muted">No peers configured</td></tr>'
        
        # Replace template variables
        html = template.replace("{{ node_address }}", self.node_address)
        html = html.replace("{{ total_peers }}", str(total_peers))
        html = html.replace("{{ healthy_peers }}", str(healthy_peers))
        html = html.replace("{{ unhealthy_peers }}", str(unhealthy_peers))
        html = html.replace("{{ unknown_peers }}", str(unknown_peers))
        html = html.replace("{{ peer_table }}", peer_table)
        html = html.replace("{{ health_check_interval }}", str(self.health_check_interval))
        html = html.replace("{{ last_updated }}", datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return html
