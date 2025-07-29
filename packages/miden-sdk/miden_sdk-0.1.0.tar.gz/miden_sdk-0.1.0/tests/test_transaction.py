"""
Tests for the Transaction class.
"""

import json
import pytest
import subprocess
from unittest.mock import patch, MagicMock, mock_open

from miden_sdk import Transaction, InvalidTransactionError, ProofGenerationError, NoteType
from miden_sdk.config import MIDEN_CLIENT_BINARY


class TestTransaction:
    """Test cases for the Transaction class."""
    
    def test_init(self):
        """Test initialization."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        data = {
            "id": "0x1234567890abcdef",
            "type": "pay_to_id",
            "sender": "0xabcdef1234567890",
            "recipient": "0x0987654321fedcba",
            "amount": 100,
            "asset_id": "0x01"
        }
        
        # Test
        tx = Transaction(data=data, sender=mock_sender)
        
        # Assertions
        assert tx.id == "0x1234567890abcdef"
        assert tx.data == data
        assert tx.sender == mock_sender
        assert tx.proof is None
    
    def test_init_with_proof(self):
        """Test initialization with proof."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        data = {
            "id": "0x1234567890abcdef",
            "type": "pay_to_id",
            "sender": "0xabcdef1234567890",
            "recipient": "0x0987654321fedcba",
            "amount": 100,
            "asset_id": "0x01"
        }
        
        proof = "some proof data"
        
        # Test
        tx = Transaction(data=data, sender=mock_sender, proof=proof)
        
        # Assertions
        assert tx.id == "0x1234567890abcdef"
        assert tx.data == data
        assert tx.sender == mock_sender
        assert tx.proof == proof
    
    def test_pay_to_id_valid(self):
        """Test pay_to_id class method with valid parameters."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        # Test
        tx = Transaction.pay_to_id(
            sender=mock_sender,
            recipient_address="0x0987654321fedcba",
            amount=100,
            asset_id="0x01",
            note_type=NoteType.PRIVATE,
            memo="Test payment"
        )
        
        # Assertions
        assert tx.data["type"] == "pay_to_id"
        assert tx.data["sender"] == "0xabcdef1234567890"
        assert tx.data["recipient"] == "0x0987654321fedcba"
        assert tx.data["amount"] == 100
        assert tx.data["asset_id"] == "0x01"
        assert tx.data["note_type"] == "private"
        assert tx.data["memo"] == "Test payment"
        assert "timestamp" in tx.data
    
    def test_pay_to_id_invalid_recipient(self):
        """Test pay_to_id with invalid recipient address."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        # Test & Assertions
        with pytest.raises(InvalidTransactionError):
            Transaction.pay_to_id(
                sender=mock_sender,
                recipient_address="invalid-address",
                amount=100
            )
    
    def test_pay_to_id_invalid_amount(self):
        """Test pay_to_id with invalid amount."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        # Test & Assertions
        with pytest.raises(InvalidTransactionError):
            Transaction.pay_to_id(
                sender=mock_sender,
                recipient_address="0x0987654321fedcba",
                amount=0
            )
    
    def test_pay_to_id_invalid_note_type(self):
        """Test pay_to_id with invalid note type."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        # Test & Assertions
        with pytest.raises(InvalidTransactionError):
            Transaction.pay_to_id(
                sender=mock_sender,
                recipient_address="0x0987654321fedcba",
                amount=100,
                note_type="invalid"
            )
    
    def test_mint_valid(self):
        """Test mint class method with valid parameters."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        # Test
        tx = Transaction.mint(
            sender=mock_sender,
            recipient_address="0x0987654321fedcba",
            amount=100,
            asset_id="0x01",
            memo="Test mint"
        )
        
        # Assertions
        assert tx.data["type"] == "mint"
        assert tx.data["sender"] == "0xabcdef1234567890"
        assert tx.data["recipient"] == "0x0987654321fedcba"
        assert tx.data["amount"] == 100
        assert tx.data["asset_id"] == "0x01"
        assert tx.data["memo"] == "Test mint"
        assert "timestamp" in tx.data
    
    def test_mint_invalid_recipient(self):
        """Test mint with invalid recipient address."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        # Test & Assertions
        with pytest.raises(InvalidTransactionError):
            Transaction.mint(
                sender=mock_sender,
                recipient_address="invalid-address",
                amount=100
            )
    
    def test_mint_invalid_amount(self):
        """Test mint with invalid amount."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        # Test & Assertions
        with pytest.raises(InvalidTransactionError):
            Transaction.mint(
                sender=mock_sender,
                recipient_address="0x0987654321fedcba",
                amount=0
            )
    
    @patch('subprocess.run')
    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_proof_success(self, mock_file, mock_json_dump, mock_run):
        """Test generate_proof success."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        data = {
            "id": "0x1234567890abcdef",
            "type": "pay_to_id",
            "sender": "0xabcdef1234567890",
            "recipient": "0x0987654321fedcba",
            "amount": 100,
            "asset_id": "0x01"
        }
        
        tx = Transaction(data=data, sender=mock_sender)
        
        # Setup mock subprocess result
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "proof data"
        mock_run.return_value = mock_result
        
        # Test
        tx.generate_proof()
        
        # Assertions
        mock_file.assert_called()
        mock_json_dump.assert_called_once_with(data, mock_file())
        mock_run.assert_called_once_with(
            [MIDEN_CLIENT_BINARY, "tx", "prove", "--input", f"tx_{tx.id}.json"],
            capture_output=True,
            text=True,
            timeout=300
        )
        assert tx.proof == "proof data"
    
    @patch('subprocess.run')
    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_proof_failure(self, mock_file, mock_json_dump, mock_run):
        """Test generate_proof failure."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        data = {
            "id": "0x1234567890abcdef",
            "type": "pay_to_id",
            "sender": "0xabcdef1234567890",
            "recipient": "0x0987654321fedcba",
            "amount": 100,
            "asset_id": "0x01"
        }
        
        tx = Transaction(data=data, sender=mock_sender)
        
        # Setup mock subprocess result with error
        mock_result = MagicMock()
        mock_result.returncode = 1
        mock_result.stderr = "Error generating proof"
        mock_run.return_value = mock_result
        
        # Test & Assertions
        with pytest.raises(ProofGenerationError):
            tx.generate_proof()
    
    @patch('subprocess.run')
    @patch('json.dump')
    @patch('builtins.open', new_callable=mock_open)
    def test_generate_proof_timeout(self, mock_file, mock_json_dump, mock_run):
        """Test generate_proof timeout."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        data = {
            "id": "0x1234567890abcdef",
            "type": "pay_to_id",
            "sender": "0xabcdef1234567890",
            "recipient": "0x0987654321fedcba",
            "amount": 100,
            "asset_id": "0x01"
        }
        
        tx = Transaction(data=data, sender=mock_sender)
        
        # Setup mock subprocess with timeout error
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="miden-client", timeout=300)
        
        # Test & Assertions
        with pytest.raises(ProofGenerationError):
            tx.generate_proof()
    
    def test_to_dict(self):
        """Test to_dict method."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        data = {
            "id": "0x1234567890abcdef",
            "type": "pay_to_id",
            "sender": "0xabcdef1234567890",
            "recipient": "0x0987654321fedcba",
            "amount": 100,
            "asset_id": "0x01"
        }
        
        proof = "proof data"
        
        tx = Transaction(data=data, sender=mock_sender, proof=proof)
        
        # Test
        result = tx.to_dict()
        
        # Assertions
        expected = {
            "id": "0x1234567890abcdef",
            "data": data,
            "proof": proof
        }
        assert result == expected
    
    def test_to_dict_no_proof(self):
        """Test to_dict method with no proof."""
        # Setup
        mock_sender = MagicMock()
        mock_sender.account_id = "0xabcdef1234567890"
        
        data = {
            "id": "0x1234567890abcdef",
            "type": "pay_to_id",
            "sender": "0xabcdef1234567890",
            "recipient": "0x0987654321fedcba",
            "amount": 100,
            "asset_id": "0x01"
        }
        
        tx = Transaction(data=data, sender=mock_sender)
        
        # Test
        result = tx.to_dict()
        
        # Assertions
        expected = {
            "id": "0x1234567890abcdef",
            "data": data
        }
        assert result == expected


if __name__ == '__main__':
    pytest.main(['-xvs', __file__]) 