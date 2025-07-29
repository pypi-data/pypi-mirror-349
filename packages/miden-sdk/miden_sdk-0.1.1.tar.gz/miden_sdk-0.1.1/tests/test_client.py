"""
Tests for the MidenClient class.
"""

import os
import pytest
from unittest.mock import patch, MagicMock

from miden_sdk import MidenClient, NodeCommunicationError, WasmError


class TestMidenClient:
    """Test cases for the MidenClient class."""
    
    def test_init_default_values(self):
        """Test initialization with default values."""
        client = MidenClient()
        assert client.rpc_endpoint == "http://18.203.155.106:57291"
        assert client.timeout == 30
    
    def test_init_custom_values(self):
        """Test initialization with custom values."""
        client = MidenClient(
            rpc_endpoint="http://custom-endpoint:8000",
            timeout=60
        )
        assert client.rpc_endpoint == "http://custom-endpoint:8000"
        assert client.timeout == 60
    
    @patch('requests.request')
    def test_make_request_success(self, mock_request):
        """Test successful request."""
        # Setup mock
        mock_response = MagicMock()
        mock_response.json.return_value = {"result": "success"}
        mock_response.raise_for_status = MagicMock()
        mock_request.return_value = mock_response
        
        # Test
        client = MidenClient()
        result = client._make_request("GET", "/test", params={"param": "value"})
        
        # Assertions
        assert result == {"result": "success"}
        mock_request.assert_called_once_with(
            method="GET",
            url="http://18.203.155.106:57291/test",
            params={"param": "value"},
            json=None,
            timeout=30
        )
    
    @patch('requests.request')
    def test_make_request_error(self, mock_request):
        """Test request with error."""
        # Setup mock
        mock_request.side_effect = Exception("Request failed")
        
        # Test
        client = MidenClient()
        
        # Assertions
        with pytest.raises(NodeCommunicationError):
            client._make_request("GET", "/test")
    
    @patch('os.path.exists')
    @patch('wasmtime.Module.from_file')
    def test_init_wasm_file_not_found(self, mock_from_file, mock_exists):
        """Test WASM initialization when file not found."""
        # Setup mock
        mock_exists.return_value = False
        
        # Test
        client = MidenClient()
        
        # Assertions
        assert client._instance is None
        mock_from_file.assert_not_called()
    
    @patch('os.path.exists')
    @patch('wasmtime.Module.from_file')
    def test_init_wasm_error(self, mock_from_file, mock_exists):
        """Test WASM initialization with error."""
        # Setup mock
        mock_exists.return_value = True
        mock_from_file.side_effect = Exception("WASM error")
        
        # Test and assertions
        with pytest.raises(WasmError):
            client = MidenClient()


if __name__ == '__main__':
    pytest.main(['-xvs', __file__]) 