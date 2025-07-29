"""
Polygon Miden Python SDK

A Python SDK for interacting with the Polygon Miden blockchain.
"""

__version__ = "0.1.0"


# Custom exceptions
class MidenError(Exception):
    """Base exception for all Miden SDK errors."""
    pass


class NodeCommunicationError(MidenError):
    """Raised when communication with the Miden node fails."""
    pass


class InvalidAccountError(MidenError):
    """Raised when an account is invalid or cannot be accessed."""
    pass


class ProofGenerationError(MidenError):
    """Raised when STARK proof generation fails."""
    pass


class InvalidNoteError(MidenError):
    """Raised when a note is invalid or cannot be processed."""
    pass


class InvalidTransactionError(MidenError):
    """Raised when a transaction is invalid or cannot be processed."""
    pass


class WasmError(MidenError):
    """Raised when there is an error with WASM operations."""
    pass


# Import main components for easier access
from miden_sdk.client import MidenClient
from miden_sdk.wallet import Wallet, Account
from miden_sdk.transaction import Transaction
from miden_sdk.note import Note
from miden_sdk.config import NoteType, AccountType

# Export common components
__all__ = [
    'MidenClient',
    'Wallet',
    'Account',
    'Transaction',
    'Note',
    'NoteType',
    'AccountType',
    'MidenError',
    'NodeCommunicationError',
    'InvalidAccountError',
    'ProofGenerationError',
    'InvalidNoteError',
    'InvalidTransactionError',
    'WasmError',
] 