"""
Wallet and account management for Miden blockchain.

This module provides classes for creating and managing wallets and accounts.
"""

import json
import os
from typing import Any, Dict, List, Optional, Union

from miden_sdk import InvalidAccountError
from miden_sdk.utils import load_json, save_json, validate_address


class Account:
    """
    Represents a Miden account.
    
    Parameters
    ----------
    account_id : str
        The account ID
    storage_mode : str
        Storage mode (private or public)
    mutable : bool
        Whether the account is mutable
    metadata : Dict[str, Any], optional
        Additional metadata for the account
        
    Attributes
    ----------
    account_id : str
        The account ID
    storage_mode : str
        Storage mode (private or public)
    mutable : bool
        Whether the account is mutable
    metadata : Dict[str, Any]
        Additional metadata for the account
    """
    
    def __init__(
        self,
        account_id: str,
        storage_mode: str,
        mutable: bool,
        metadata: Optional[Dict[str, Any]] = None
    ):
        if not validate_address(account_id):
            raise InvalidAccountError(f"Invalid account ID format: {account_id}")
            
        if storage_mode not in ["private", "public"]:
            raise ValueError("Storage mode must be 'private' or 'public'")
            
        self.account_id = account_id
        self.storage_mode = storage_mode
        self.mutable = mutable
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the account to a dictionary.
        
        Returns
        -------
        Dict[str, Any]
            Account as a dictionary
        """
        return {
            "account_id": self.account_id,
            "storage_mode": self.storage_mode,
            "mutable": self.mutable,
            "metadata": self.metadata
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Account':
        """
        Create an account from a dictionary.
        
        Parameters
        ----------
        data : Dict[str, Any]
            Account data
            
        Returns
        -------
        Account
            Account instance
        """
        return cls(
            account_id=data["account_id"],
            storage_mode=data["storage_mode"],
            mutable=data["mutable"],
            metadata=data.get("metadata", {})
        )


class Wallet:
    """
    Represents a Miden wallet.
    
    A wallet contains an account along with the necessary keys and metadata
    for managing it.
    
    Parameters
    ----------
    account_id : str
        The account ID
    client : MidenClient, optional
        MidenClient instance for node communication
    storage_mode : str, optional
        Storage mode (private or public)
    mutable : bool, optional
        Whether the wallet is mutable
    keypair : Dict[str, str], optional
        Keypair for the wallet
    metadata : Dict[str, Any], optional
        Additional metadata for the wallet
        
    Attributes
    ----------
    account_id : str
        The account ID
    client : MidenClient
        MidenClient instance for node communication
    account : Account
        The account associated with this wallet
    keypair : Dict[str, str]
        Keypair for the wallet
    metadata : Dict[str, Any]
        Additional metadata for the wallet
    """
    
    def __init__(
        self,
        account_id: str,
        client: Optional['MidenClient'] = None,
        storage_mode: str = "private",
        mutable: bool = True,
        keypair: Optional[Dict[str, str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        self.account_id = account_id
        self.client = client
        self.account = Account(
            account_id=account_id,
            storage_mode=storage_mode,
            mutable=mutable,
            metadata=metadata
        )
        self.keypair = keypair or self._generate_keypair()
        self.metadata = metadata or {}
    
    def _generate_keypair(self) -> Dict[str, str]:
        """
        Generate a new keypair for the wallet.
        
        Returns
        -------
        Dict[str, str]
            Generated keypair with 'private_key' and 'public_key'
        """
        # In a real implementation, this would generate a proper cryptographic keypair
        # For now, we'll just use some placeholder values
        return {
            "private_key": f"private_key_for_{self.account_id}",
            "public_key": f"public_key_for_{self.account_id}"
        }
    
    def save(self, file_path: str) -> None:
        """
        Save the wallet to a file.
        
        Parameters
        ----------
        file_path : str
            Path to save the wallet to
        """
        data = {
            "account_id": self.account_id,
            "storage_mode": self.account.storage_mode,
            "mutable": self.account.mutable,
            "keypair": self.keypair,
            "metadata": self.metadata
        }
        
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    @classmethod
    def load(cls, file_path: str, client: Optional['MidenClient'] = None) -> 'Wallet':
        """
        Load a wallet from a file.
        
        Parameters
        ----------
        file_path : str
            Path to load the wallet from
        client : MidenClient, optional
            MidenClient instance for node communication
            
        Returns
        -------
        Wallet
            Loaded wallet instance
            
        Raises
        ------
        FileNotFoundError
            If the file does not exist
        """
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        return cls(
            account_id=data["account_id"],
            client=client,
            storage_mode=data["storage_mode"],
            mutable=data["mutable"],
            keypair=data["keypair"],
            metadata=data.get("metadata", {})
        )
    
    def get_balance(self) -> Dict[str, int]:
        """
        Get the account balance from the node.
        
        Returns
        -------
        Dict[str, int]
            Asset balances
            
        Raises
        ------
        NodeCommunicationError
            If there's an error communicating with the node
        """
        if not self.client:
            raise ValueError("Client not set. Use Wallet.load(file_path, client) to set a client.")
            
        # Get account data from the node
        account_data = self.client.get_account(self.account_id)
        
        # Extract balances
        return account_data.get("balances", {}) 