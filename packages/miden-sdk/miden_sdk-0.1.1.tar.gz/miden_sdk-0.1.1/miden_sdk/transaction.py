"""
Transaction building and management for Miden blockchain.

This module provides the Transaction class for building, serializing,
and submitting transactions to the Miden blockchain.
"""

import json
import logging
import subprocess
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from miden_sdk import InvalidTransactionError, ProofGenerationError
from miden_sdk.config import MIDEN_CLIENT_BINARY, DEFAULT_PROOF_TIMEOUT, NoteType
from miden_sdk.utils import hash_data, validate_address


# Configure logger
logger = logging.getLogger(__name__)


class Transaction:
    """
    Represents a Miden transaction.
    
    Parameters
    ----------
    data : Dict[str, Any]
        Transaction data
    sender : str
        The sender's wallet or account
    proof : str, optional
        STARK proof for the transaction
        
    Attributes
    ----------
    id : str
        Transaction ID
    data : Dict[str, Any]
        Transaction data
    sender : str
        The sender's wallet or account
    proof : str
        STARK proof for the transaction
    """
    
    def __init__(
        self, 
        data: Dict[str, Any],
        sender: 'Wallet',
        proof: Optional[str] = None
    ):
        self.id = data.get("id", f"0x{uuid.uuid4().hex}")
        self.data = data
        if "id" not in self.data:
            self.data["id"] = self.id
        self.sender = sender
        self.proof = proof
    
    @classmethod
    def pay_to_id(
        cls,
        sender: 'Wallet',
        recipient_address: str,
        amount: int,
        asset_id: str = "0x01",  # Default asset ID
        note_type: str = NoteType.PRIVATE,
        memo: str = ""
    ) -> 'Transaction':
        """
        Create a payment transaction.
        
        Parameters
        ----------
        sender : Wallet
            The sender's wallet
        recipient_address : str
            The recipient's account ID
        amount : int
            The amount to transfer
        asset_id : str, optional
            The asset ID to transfer
        note_type : str, optional
            The type of note to create (private or public)
        memo : str, optional
            Optional memo for the transaction
            
        Returns
        -------
        Transaction
            A new transaction instance
            
        Raises
        ------
        InvalidTransactionError
            If the transaction parameters are invalid
        """
        # Validate parameters
        if not validate_address(recipient_address):
            raise InvalidTransactionError(f"Invalid recipient address: {recipient_address}")
        
        if amount <= 0:
            raise InvalidTransactionError(f"Invalid amount: {amount}")
        
        if note_type not in [NoteType.PRIVATE, NoteType.PUBLIC]:
            raise InvalidTransactionError(f"Invalid note type: {note_type}")
        
        # Create transaction data
        tx_data = {
            "id": f"0x{uuid.uuid4().hex}",
            "type": "pay_to_id",
            "sender": sender.account_id,
            "recipient": recipient_address,
            "amount": amount,
            "asset_id": asset_id,
            "note_type": note_type,
            "memo": memo,
            "timestamp": int(datetime.now().timestamp())
        }
        
        return cls(data=tx_data, sender=sender)
    
    @classmethod
    def mint(
        cls,
        sender: 'Wallet',
        recipient_address: str,
        amount: int,
        asset_id: str = "0x01",  # Default asset ID
        memo: str = ""
    ) -> 'Transaction':
        """
        Create a mint transaction (for faucets).
        
        Parameters
        ----------
        sender : Wallet
            The sender's wallet (must be a faucet account)
        recipient_address : str
            The recipient's account ID
        amount : int
            The amount to mint
        asset_id : str, optional
            The asset ID to mint
        memo : str, optional
            Optional memo for the transaction
            
        Returns
        -------
        Transaction
            A new transaction instance
            
        Raises
        ------
        InvalidTransactionError
            If the transaction parameters are invalid
        """
        # Validate parameters
        if not validate_address(recipient_address):
            raise InvalidTransactionError(f"Invalid recipient address: {recipient_address}")
        
        if amount <= 0:
            raise InvalidTransactionError(f"Invalid amount: {amount}")
        
        # Create transaction data
        tx_data = {
            "id": f"0x{uuid.uuid4().hex}",
            "type": "mint",
            "sender": sender.account_id,
            "recipient": recipient_address,
            "amount": amount,
            "asset_id": asset_id,
            "memo": memo,
            "timestamp": int(datetime.now().timestamp())
        }
        
        return cls(data=tx_data, sender=sender)
    
    def generate_proof(self, timeout: int = DEFAULT_PROOF_TIMEOUT) -> None:
        """
        Generate a STARK proof for the transaction using the miden-client CLI.
        
        Parameters
        ----------
        timeout : int, optional
            Timeout for proof generation in seconds
            
        Raises
        ------
        ProofGenerationError
            If proof generation fails
        """
        # Write transaction data to a temporary file
        temp_file = f"tx_{self.id}.json"
        with open(temp_file, 'w') as f:
            json.dump(self.data, f)
        
        # Use miden-client to generate proof
        cmd = [MIDEN_CLIENT_BINARY, "tx", "prove", "--input", temp_file]
        
        try:
            logger.info(f"Generating proof for transaction {self.id}")
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            if result.returncode != 0:
                raise ProofGenerationError(f"Proof generation failed: {result.stderr}")
            
            # Parse output to get proof
            self.proof = result.stdout.strip()
            logger.info(f"Proof generated successfully for transaction {self.id}")
            
        except subprocess.TimeoutExpired:
            raise ProofGenerationError(f"Proof generation timed out after {timeout} seconds")
        except subprocess.SubprocessError as e:
            raise ProofGenerationError(f"Error executing miden-client: {str(e)}")
        finally:
            # Clean up temporary file
            try:
                import os
                os.remove(temp_file)
            except:
                pass
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the transaction to a dictionary.
        
        Returns
        -------
        Dict[str, Any]
            Transaction as a dictionary
        """
        result = {
            "id": self.id,
            "data": self.data
        }
        
        if self.proof:
            result["proof"] = self.proof
            
        return result
    
    def save(self, file_path: str) -> None:
        """
        Save the transaction to a file.
        
        Parameters
        ----------
        file_path : str
            Path to save the transaction to
        """
        with open(file_path, 'w') as f:
            json.dump(self.to_dict(), f, indent=2)
    
    @classmethod
    def load(cls, file_path: str, sender: 'Wallet') -> 'Transaction':
        """
        Load a transaction from a file.
        
        Parameters
        ----------
        file_path : str
            Path to load the transaction from
        sender : Wallet
            The sender's wallet
            
        Returns
        -------
        Transaction
            Loaded transaction instance
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
            
        tx_data = data.get("data", {})
        proof = data.get("proof")
        
        return cls(data=tx_data, sender=sender, proof=proof) 