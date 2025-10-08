"""Tests for the cluster CLI module."""

import pytest
from eleventh.decks.cluster import extract_host_port


class TestExtractHostPort:
    """Tests for host and port extraction."""
    
    def test_extract_from_http_address(self):
        """Test extracting host and port from http address."""
        host, port = extract_host_port("http://127.0.0.1:8001")
        assert host == "127.0.0.1"
        assert port == 8001
    
    def test_extract_from_https_address(self):
        """Test extracting host and port from https address."""
        host, port = extract_host_port("https://example.com:9000")
        assert host == "example.com"
        assert port == 9000
    
    def test_extract_from_localhost(self):
        """Test extracting from localhost address."""
        host, port = extract_host_port("http://localhost:8080")
        assert host == "localhost"
        assert port == 8080
    
    def test_invalid_address_no_port(self):
        """Test error handling for address without port."""
        with pytest.raises(ValueError, match="Invalid address format"):
            extract_host_port("http://127.0.0.1")
    
    def test_invalid_port_format(self):
        """Test error handling for invalid port."""
        with pytest.raises(ValueError, match="Invalid port in address"):
            extract_host_port("http://127.0.0.1:abc")
