"""
Utility functions for the Miden Python SDK.

This module contains helper functions for hashing, encoding, and other common
operations used throughout the SDK.
"""

import base64
import hashlib
import json
import os
from typing import Any, Dict, List, Optional, Union

import blake3


def hash_data(data: Union[str, bytes]) -> str:
    """
    Hash data using blake3 algorithm.
    
    Parameters
    ----------
    data : Union[str, bytes]
        The data to hash
        
    Returns
    -------
    str
        The hex-encoded hash
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return blake3.blake3(data).hexdigest()


def encode_base64(data: Union[str, bytes]) -> str:
    """
    Encode data to base64.
    
    Parameters
    ----------
    data : Union[str, bytes]
        The data to encode
        
    Returns
    -------
    str
        The base64-encoded string
    """
    if isinstance(data, str):
        data = data.encode('utf-8')
    return base64.b64encode(data).decode('utf-8')


def decode_base64(data: str) -> bytes:
    """
    Decode base64 data.
    
    Parameters
    ----------
    data : str
        The base64-encoded string
        
    Returns
    -------
    bytes
        The decoded data
    """
    return base64.b64decode(data)


def load_json(file_path: str) -> Dict[str, Any]:
    """
    Load JSON data from a file.
    
    Parameters
    ----------
    file_path : str
        Path to the JSON file
        
    Returns
    -------
    Dict[str, Any]
        The loaded JSON data
        
    Raises
    ------
    FileNotFoundError
        If the file does not exist
    json.JSONDecodeError
        If the file contains invalid JSON
    """
    with open(file_path, 'r') as f:
        return json.load(f)


def save_json(data: Dict[str, Any], file_path: str) -> None:
    """
    Save data to a JSON file.
    
    Parameters
    ----------
    data : Dict[str, Any]
        The data to save
    file_path : str
        Path to the output file
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)


def validate_address(address: str) -> bool:
    """
    Validate if a string is a valid Miden address (0x followed by hex characters).
    
    Parameters
    ----------
    address : str
        The address to validate
        
    Returns
    -------
    bool
        True if valid, False otherwise
    """
    if not isinstance(address, str):
        return False
        
    # Miden addresses are 0x followed by hex characters
    if not address.startswith('0x'):
        return False
        
    # Check if the rest of the string is valid hex
    try:
        int(address[2:], 16)
        return True
    except ValueError:
        return False


def to_hex(value: Union[int, bytes, str]) -> str:
    """
    Convert a value to hex string.
    
    Parameters
    ----------
    value : Union[int, bytes, str]
        The value to convert
        
    Returns
    -------
    str
        The hex-encoded string
    """
    if isinstance(value, int):
        return f"0x{value:x}"
    elif isinstance(value, bytes):
        return f"0x{value.hex()}"
    elif isinstance(value, str):
        if value.startswith('0x'):
            return value
        return f"0x{value}"
    else:
        raise TypeError(f"Cannot convert {type(value)} to hex")


def from_hex(hex_str: str) -> bytes:
    """
    Convert a hex string to bytes.
    
    Parameters
    ----------
    hex_str : str
        The hex string
        
    Returns
    -------
    bytes
        The decoded bytes
    """
    if hex_str.startswith('0x'):
        hex_str = hex_str[2:]
    return bytes.fromhex(hex_str) 