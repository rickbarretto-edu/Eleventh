"""Tests for the Consul Plugin."""

import asyncio
import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from eleventh.clusters import ConsulPlugin, PeerStatus


@pytest.fixture
def app_with_plugin():
    """Create a FastAPI app with the ConsulPlugin attached."""
    app = FastAPI()
    
    @app.get("/")
    async def root():
        return {"message": "Hello"}
    
    plugin = ConsulPlugin(
        nodes=[
            "http://127.0.0.1:8001",
            "http://127.0.0.1:8002",
            "http://127.0.0.1:8003",
        ],
        health_check_interval=1.0,
    )
    plugin.attach(app, node_address="http://127.0.0.1:8001")
    
    return app


@pytest.mark.asyncio
async def test_health_endpoint(app_with_plugin):
    """Test the /cluster/health endpoint."""
    async with AsyncClient(
        transport=ASGITransport(app=app_with_plugin), 
        base_url="http://test"
    ) as client:
        response = await client.get("/cluster/health")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["status"] == "healthy"
        assert data["node_address"] == "http://127.0.0.1:8001"
        assert "timestamp" in data
        assert "version" in data


@pytest.mark.asyncio
async def test_cluster_status_endpoint(app_with_plugin):
    """Test the /cluster/status endpoint."""
    async with AsyncClient(
        transport=ASGITransport(app=app_with_plugin), 
        base_url="http://test"
    ) as client:
        response = await client.get("/cluster/status")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["node_address"] == "http://127.0.0.1:8001"
        assert data["cluster_size"] == 3  # 2 peers + 1 this node
        assert len(data["peers"]) == 2
        assert "healthy_peers" in data
        assert "last_updated" in data


@pytest.mark.asyncio
async def test_list_peers_endpoint(app_with_plugin):
    """Test the /cluster/peers endpoint."""
    async with AsyncClient(
        transport=ASGITransport(app=app_with_plugin), 
        base_url="http://test"
    ) as client:
        response = await client.get("/cluster/peers")
        
        assert response.status_code == 200
        data = response.json()
        
        assert data["node_address"] == "http://127.0.0.1:8001"
        assert len(data["peers"]) == 2
        assert "http://127.0.0.1:8002" in data["peers"]
        assert "http://127.0.0.1:8003" in data["peers"]
        assert data["total_peers"] == 2


@pytest.mark.asyncio
async def test_add_peer_endpoint(app_with_plugin):
    """Test adding a peer via the /cluster/peers/add endpoint."""
    async with AsyncClient(
        transport=ASGITransport(app=app_with_plugin), 
        base_url="http://test"
    ) as client:
        # Add a new peer
        response = await client.post(
            "/cluster/peers/add",
            params={"peer_address": "http://127.0.0.1:8004"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Verify it was added
        response = await client.get("/cluster/peers")
        data = response.json()
        assert "http://127.0.0.1:8004" in data["peers"]
        assert data["total_peers"] == 3


@pytest.mark.asyncio
async def test_add_duplicate_peer(app_with_plugin):
    """Test adding a duplicate peer returns success=False."""
    async with AsyncClient(
        transport=ASGITransport(app=app_with_plugin), 
        base_url="http://test"
    ) as client:
        # Try to add an existing peer
        response = await client.post(
            "/cluster/peers/add",
            params={"peer_address": "http://127.0.0.1:8002"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "already exists" in data["message"]


@pytest.mark.asyncio
async def test_remove_peer_endpoint(app_with_plugin):
    """Test removing a peer via the /cluster/peers/remove endpoint."""
    async with AsyncClient(
        transport=ASGITransport(app=app_with_plugin), 
        base_url="http://test"
    ) as client:
        # Remove a peer
        response = await client.delete(
            "/cluster/peers/remove",
            params={"peer_address": "http://127.0.0.1:8002"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        
        # Verify it was removed
        response = await client.get("/cluster/peers")
        data = response.json()
        assert "http://127.0.0.1:8002" not in data["peers"]
        assert data["total_peers"] == 1


@pytest.mark.asyncio
async def test_remove_nonexistent_peer(app_with_plugin):
    """Test removing a nonexistent peer returns success=False."""
    async with AsyncClient(
        transport=ASGITransport(app=app_with_plugin), 
        base_url="http://test"
    ) as client:
        response = await client.delete(
            "/cluster/peers/remove",
            params={"peer_address": "http://127.0.0.1:9999"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is False
        assert "not found" in data["message"]


@pytest.mark.asyncio
async def test_admin_page_renders(app_with_plugin):
    """Test that the admin page renders HTML."""
    async with AsyncClient(
        transport=ASGITransport(app=app_with_plugin), 
        base_url="http://test"
    ) as client:
        response = await client.get("/cluster/admin")
        
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]
        
        # Check for key HTML elements
        html = response.text
        assert "Cluster Administration" in html
        assert "http://127.0.0.1:8001" in html
        assert "Peer Health Status" in html


@pytest.mark.asyncio
async def test_plugin_initialization():
    """Test plugin initialization with different configurations."""
    # With multiple nodes
    plugin1 = ConsulPlugin(
        nodes=[
            "http://127.0.0.1:8001",
            "http://127.0.0.1:8002",
        ],
    )
    assert len(plugin1.nodes) == 2
    assert plugin1.health_check_interval == 10.0
    assert plugin1.node_address is None  # Not set until attach()
    
    # Single node
    plugin2 = ConsulPlugin(
        nodes=["http://127.0.0.1:8001"],
    )
    assert len(plugin2.nodes) == 1
    
    # Custom intervals
    plugin3 = ConsulPlugin(
        nodes=["http://127.0.0.1:8001", "http://127.0.0.1:8002"],
        health_check_interval=5.0,
        health_check_timeout=2.0,
    )
    assert plugin3.health_check_interval == 5.0
    assert plugin3.health_check_timeout == 2.0
    
    # Test attach with valid node address
    app = FastAPI()
    plugin1.attach(app, node_address="http://127.0.0.1:8001")
    assert plugin1.node_address == "http://127.0.0.1:8001"
    assert plugin1.peers == ["http://127.0.0.1:8002"]
    
    # Test attach with invalid node address
    app2 = FastAPI()
    plugin4 = ConsulPlugin(nodes=["http://127.0.0.1:8001"])
    with pytest.raises(ValueError, match="must be in the nodes list"):
        plugin4.attach(app2, node_address="http://127.0.0.1:9999")


@pytest.mark.asyncio
async def test_peer_status_model():
    """Test the PeerStatus model."""
    status = PeerStatus(
        address="http://127.0.0.1:8001",
        status="healthy",
        last_check=1234567890.0,
        last_success=1234567890.0,
        response_time_ms=50.5,
    )
    
    assert status.address == "http://127.0.0.1:8001"
    assert status.status == "healthy"
    assert status.response_time_ms == 50.5
    assert status.error is None


@pytest.mark.asyncio
async def test_plugin_startup_and_shutdown(app_with_plugin):
    """Test that plugin starts and stops cleanly."""
    # The plugin should start when the app context is entered
    async with AsyncClient(
        transport=ASGITransport(app=app_with_plugin), 
        base_url="http://test"
    ) as client:
        # Make a request to ensure app is running
        response = await client.get("/cluster/health")
        assert response.status_code == 200
    
    # After exiting, the plugin should clean up
    # (This is implicit in the async context manager)
