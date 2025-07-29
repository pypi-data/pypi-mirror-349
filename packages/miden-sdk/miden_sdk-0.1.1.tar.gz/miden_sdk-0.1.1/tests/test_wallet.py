"""
Tests for the Wallet and Account classes.
"""

import os
import json
import pytest
from unittest.mock import patch, MagicMock, mock_open

from miden_sdk import Wallet, Account, InvalidAccountError
from miden_sdk.utils import save_json


class TestAccount:
    """Test cases for the Account class."""
    
    def test_init_valid(self):
        """Test initialization with valid parameters."""
        account = Account(
            account_id="0xabcdef1234567890",
            storage_mode="private",
            mutable=True
        )
        assert account.account_id == "0xabcdef1234567890"
        assert account.storage_mode == "private"
        assert account.mutable is True
        assert account.metadata == {}
    
    def test_init_invalid_account_id(self):
        """Test initialization with invalid account ID."""
        with pytest.raises(InvalidAccountError):
            Account(
                account_id="invalid-id",
                storage_mode="private",
                mutable=True
            )
    
    def test_init_invalid_storage_mode(self):
        """Test initialization with invalid storage mode."""
        with pytest.raises(ValueError):
            Account(
                account_id="0xabcdef1234567890",
                storage_mode="invalid",
                mutable=True
            )
    
    def test_to_dict(self):
        """Test to_dict method."""
        account = Account(
            account_id="0xabcdef1234567890",
            storage_mode="private",
            mutable=True,
            metadata={"key": "value"}
        )
        result = account.to_dict()
        expected = {
            "account_id": "0xabcdef1234567890",
            "storage_mode": "private",
            "mutable": True,
            "metadata": {"key": "value"}
        }
        assert result == expected
    
    def test_from_dict(self):
        """Test from_dict method."""
        data = {
            "account_id": "0xabcdef1234567890",
            "storage_mode": "private",
            "mutable": True,
            "metadata": {"key": "value"}
        }
        account = Account.from_dict(data)
        assert account.account_id == "0xabcdef1234567890"
        assert account.storage_mode == "private"
        assert account.mutable is True
        assert account.metadata == {"key": "value"}


class TestWallet:
    """Test cases for the Wallet class."""
    
    def test_init_valid(self):
        """Test initialization with valid parameters."""
        wallet = Wallet(
            account_id="0xabcdef1234567890",
            storage_mode="private",
            mutable=True
        )
        assert wallet.account_id == "0xabcdef1234567890"
        assert wallet.account.storage_mode == "private"
        assert wallet.account.mutable is True
        assert wallet.keypair is not None
        assert "private_key" in wallet.keypair
        assert "public_key" in wallet.keypair
    
    def test_init_with_keypair(self):
        """Test initialization with provided keypair."""
        keypair = {
            "private_key": "test_private_key",
            "public_key": "test_public_key"
        }
        wallet = Wallet(
            account_id="0xabcdef1234567890",
            storage_mode="private",
            mutable=True,
            keypair=keypair
        )
        assert wallet.keypair == keypair
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.dump')
    def test_save(self, mock_json_dump, mock_open_file):
        """Test save method."""
        wallet = Wallet(
            account_id="0xabcdef1234567890",
            storage_mode="private",
            mutable=True
        )
        wallet.save("wallet.json")
        
        # Check that the file was opened correctly
        mock_open_file.assert_called_once_with('wallet.json', 'w')
        
        # Check that json.dump was called with the correct data
        mock_json_dump.assert_called_once()
        args, _ = mock_json_dump.call_args
        data, file_handle = args
        
        assert data["account_id"] == "0xabcdef1234567890"
        assert data["storage_mode"] == "private"
        assert data["mutable"] is True
        assert "keypair" in data
    
    @patch('builtins.open', new_callable=mock_open)
    @patch('json.load')
    def test_load(self, mock_json_load, mock_open_file):
        """Test load method."""
        # Create mock data for json.load to return
        mock_data = {
            "account_id": "0xabcdef1234567890",
            "storage_mode": "private",
            "mutable": True,
            "keypair": {
                "private_key": "test_private_key",
                "public_key": "test_public_key"
            },
            "metadata": {"key": "value"}
        }
        mock_json_load.return_value = mock_data
        
        # Call the load method
        wallet = Wallet.load("wallet.json")
        
        # Check that the file was opened correctly
        mock_open_file.assert_called_once_with("wallet.json", "r")
        
        # Check that the wallet was created with the correct data
        assert wallet.account_id == "0xabcdef1234567890"
        assert wallet.account.storage_mode == "private"
        assert wallet.account.mutable is True
        
        # This is the key assertion that was failing - with our fix it should now pass
        assert wallet.keypair == mock_data["keypair"]
        assert wallet.metadata == mock_data["metadata"]
    
    @patch('miden_sdk.client.MidenClient.get_account')
    def test_get_balance(self, mock_get_account):
        """Test get_balance method."""
        # Setup mock
        mock_client = MagicMock()
        mock_get_account.return_value = {
            "balances": {
                "0x01": 100,
                "0x02": 200
            }
        }
        mock_client.get_account = mock_get_account
        
        # Create wallet with mock client
        wallet = Wallet(
            account_id="0xabcdef1234567890",
            client=mock_client
        )
        
        # Test
        balances = wallet.get_balance()
        
        # Assertions
        assert balances == {"0x01": 100, "0x02": 200}
        mock_get_account.assert_called_once_with("0xabcdef1234567890")
    
    def test_get_balance_no_client(self):
        """Test get_balance method with no client."""
        wallet = Wallet(account_id="0xabcdef1234567890")
        
        with pytest.raises(ValueError):
            wallet.get_balance()


if __name__ == '__main__':
    pytest.main(['-xvs', __file__]) 