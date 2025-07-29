"""
Configuration settings for the Miden Python SDK.

This module contains constants, endpoint configurations, and default values
used throughout the SDK.
"""

# Default Miden node endpoint (testnet)
DEFAULT_RPC_ENDPOINT = "http://18.203.155.106:57291"

# WASM module path
DEFAULT_WASM_MODULE_PATH = "miden_sdk/wasm/miden_sdk.wasm"

# CLI configuration
MIDEN_CLIENT_BINARY = "miden-client"

# Account types
class AccountType:
    """Enum-like class for account types"""
    PRIVATE = "private"
    PUBLIC = "public"

# Note types
class NoteType:
    """Enum-like class for note types"""
    PRIVATE = "private"
    PUBLIC = "public"

# Timeouts (in seconds)
DEFAULT_REQUEST_TIMEOUT = 30
DEFAULT_PROOF_TIMEOUT = 300  # STARK proof generation can take time

# API endpoints
class Endpoints:
    """API endpoints for Miden node interaction"""
    SUBMIT_TRANSACTION = "/v1/transactions/submit"
    GET_TRANSACTION = "/v1/transactions/{tx_id}"
    GET_ACCOUNT = "/v1/accounts/{account_id}"
    GET_NOTES = "/v1/notes"
    
# Status codes
class StatusCode:
    """Status codes for Miden operations"""
    SUCCESS = "success"
    PENDING = "pending"
    FAILED = "failed" 