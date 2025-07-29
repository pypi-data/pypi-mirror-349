"""
Client for interacting with the Miden node.

This module provides the MidenClient class for communicating with a Miden node 
and executing WebAssembly (WASM) operations.
"""

import json
import logging
import os
import subprocess
from typing import Any, Dict, List, Optional, Union, TYPE_CHECKING

import requests
import wasmtime

from miden_sdk import (
    InvalidAccountError, 
    InvalidNoteError, 
    NodeCommunicationError,
    WasmError
)
from miden_sdk.config import (
    DEFAULT_RPC_ENDPOINT, 
    DEFAULT_WASM_MODULE_PATH,
    DEFAULT_REQUEST_TIMEOUT,
    Endpoints
)
from miden_sdk.utils import validate_address

# Use TYPE_CHECKING to avoid circular imports
if TYPE_CHECKING:
    from miden_sdk.transaction import Transaction
    from miden_sdk.note import Note
    from miden_sdk.wallet import Wallet

# Configure logger
logger = logging.getLogger(__name__)


class MidenClient:
    """
    Client for interacting with the Miden blockchain.
    
    This class provides methods for communicating with a Miden node and 
    executing WASM operations.
    
    Parameters
    ----------
    rpc_endpoint : str, optional
        The Miden node's RPC endpoint
    wasm_path : str, optional
        Path to the Miden SDK WASM module
    timeout : int, optional
        Timeout for RPC requests in seconds
        
    Attributes
    ----------
    rpc_endpoint : str
        The Miden node's RPC endpoint
    wasm_path : str
        Path to the Miden SDK WASM module
    timeout : int
        Timeout for RPC requests in seconds
    """
    
    def __init__(
        self,
        rpc_endpoint: str = DEFAULT_RPC_ENDPOINT,
        wasm_path: str = DEFAULT_WASM_MODULE_PATH,
        timeout: int = DEFAULT_REQUEST_TIMEOUT
    ):
        self.rpc_endpoint = rpc_endpoint
        self.wasm_path = wasm_path
        self.timeout = timeout
        
        # Initialize WASM engine if the WASM file exists
        self._store = None
        self._instance = None
        
        if os.path.exists(wasm_path):
            self._init_wasm()
        else:
            logger.warning(f"WASM module not found at {wasm_path}. WASM functionality will be unavailable.")
    
    def _init_wasm(self) -> None:
        """
        Initialize the WASM engine and load the Miden SDK module.
        
        Raises
        ------
        WasmError
            If there's an error initializing the WASM engine
        """
        try:
            self._store = wasmtime.Store()
            module = wasmtime.Module.from_file(self._store.engine, self.wasm_path)
            self._instance = wasmtime.Instance(self._store, module, [])
            logger.info("WASM module initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing WASM: {str(e)}")
            raise WasmError(f"Failed to initialize WASM module: {str(e)}")
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict[str, Any]] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the Miden node.
        
        Parameters
        ----------
        method : str
            HTTP method (GET, POST, etc.)
        endpoint : str
            API endpoint
        params : Dict[str, Any], optional
            Query parameters
        data : Dict[str, Any], optional
            Request body for POST requests
            
        Returns
        -------
        Dict[str, Any]
            Response from the node
            
        Raises
        ------
        NodeCommunicationError
            If there's an error communicating with the node
        """
        url = f"{self.rpc_endpoint}{endpoint}"
        
        try:
            response = requests.request(
                method=method,
                url=url,
                params=params,
                json=data,
                timeout=self.timeout
            )
            
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error communicating with Miden node: {str(e)}")
            raise NodeCommunicationError(f"Failed to communicate with Miden node: {str(e)}")
    
    def get_account(self, account_id: str) -> Dict[str, Any]:
        """
        Get account information from the Miden node.
        
        Parameters
        ----------
        account_id : str
            The ID of the account to retrieve
            
        Returns
        -------
        Dict[str, Any]
            Account information
            
        Raises
        ------
        InvalidAccountError
            If the account ID is invalid
        NodeCommunicationError
            If there's an error communicating with the node
        """
        if not validate_address(account_id):
            raise InvalidAccountError(f"Invalid account ID format: {account_id}")
        
        endpoint = Endpoints.GET_ACCOUNT.format(account_id=account_id)
        
        try:
            return self._make_request("GET", endpoint)
        except NodeCommunicationError as e:
            # Check if it's specifically a 404, which means the account doesn't exist
            if "404" in str(e):
                raise InvalidAccountError(f"Account not found: {account_id}")
            raise
    
    def send_transaction(self, transaction: 'Transaction') -> str:
        """
        Submit a transaction to the Miden node.
        
        Parameters
        ----------
        transaction : Transaction
            The transaction to submit
            
        Returns
        -------
        str
            Transaction ID
            
        Raises
        ------
        NodeCommunicationError
            If there's an error communicating with the node
        """
        # Import here to avoid circular imports
        from miden_sdk.transaction import Transaction
        
        if not isinstance(transaction, Transaction):
            raise TypeError("Expected a Transaction object")
        
        if not transaction.proof:
            raise ValueError("Transaction must have a proof before sending")
        
        data = {
            "data": transaction.data,
            "proof": transaction.proof
        }
        
        response = self._make_request("POST", Endpoints.SUBMIT_TRANSACTION, data=data)
        
        # Return the transaction ID
        return response.get("tx_id")
    
    def get_transaction(self, tx_id: str) -> Dict[str, Any]:
        """
        Get transaction information from the Miden node.
        
        Parameters
        ----------
        tx_id : str
            The transaction ID
            
        Returns
        -------
        Dict[str, Any]
            Transaction information
            
        Raises
        ------
        NodeCommunicationError
            If there's an error communicating with the node
        """
        if not validate_address(tx_id):
            raise ValueError(f"Invalid transaction ID format: {tx_id}")
        
        endpoint = Endpoints.GET_TRANSACTION.format(tx_id=tx_id)
        
        return self._make_request("GET", endpoint)
    
    def get_notes(self, account_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get consumable notes for an account.
        
        Parameters
        ----------
        account_id : str, optional
            The account ID to get notes for. If not provided, get all notes.
            
        Returns
        -------
        List[Dict[str, Any]]
            List of notes
            
        Raises
        ------
        NodeCommunicationError
            If there's an error communicating with the node
        """
        params = {}
        if account_id:
            if not validate_address(account_id):
                raise InvalidAccountError(f"Invalid account ID format: {account_id}")
            params["account_id"] = account_id
        
        return self._make_request("GET", Endpoints.GET_NOTES, params=params)
    
    def add_note(self, note: 'Note') -> None:
        """
        Add a note to the client's note store.
        
        Parameters
        ----------
        note : Note
            The note to add
            
        Raises
        ------
        InvalidNoteError
            If the note is invalid
        """
        # Import here to avoid circular imports
        from miden_sdk.note import Note
        
        if not isinstance(note, Note):
            raise TypeError("Expected a Note object")
            
        # Store the note locally
        # In a real implementation, this would store the note in a local database
        # For now, we'll just log it
        logger.info(f"Added note: {note.id}")
    
    def new_wallet(self, storage_mode: str = "private", mutable: bool = True) -> 'Wallet':
        """
        Create a new wallet using the WASM module.
        
        Parameters
        ----------
        storage_mode : str, optional
            Storage mode for the wallet (private or public)
        mutable : bool, optional
            Whether the wallet is mutable
            
        Returns
        -------
        Wallet
            A new wallet instance
            
        Raises
        ------
        WasmError
            If there's an error with WASM operations
        """
        # Import here to avoid circular imports
        from miden_sdk.wallet import Wallet
        
        if storage_mode not in ["private", "public"]:
            raise ValueError("Storage mode must be 'private' or 'public'")
        
        if self._instance is None:
            raise WasmError("WASM module not initialized")
            
        try:
            new_wallet_fn = self._instance.exports(self._store)["new_wallet"]
            wallet_id = new_wallet_fn(self._store, storage_mode, mutable)
            return Wallet(account_id=str(wallet_id), client=self)
        except Exception as e:
            logger.error(f"Error creating wallet via WASM: {str(e)}")
            raise WasmError(f"Failed to create wallet: {str(e)}") 