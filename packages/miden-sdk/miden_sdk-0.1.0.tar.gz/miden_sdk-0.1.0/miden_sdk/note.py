"""
Note management for Miden blockchain.

This module provides the Note class for creating and managing notes,
which represent transferable assets on the Miden blockchain.
"""

import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field

from miden_sdk import InvalidNoteError
from miden_sdk.config import NoteType
from miden_sdk.utils import hash_data, load_json, save_json, validate_address


class Note(BaseModel):
    """
    Represents a Miden note.
    
    Notes are used to transfer assets between accounts in the Miden blockchain.
    
    Parameters
    ----------
    id : str, optional
        The note ID (generated if not provided)
    sender : str
        The sender's account ID
    recipient : str
        The recipient's account ID
    amount : int
        The amount of the asset being transferred
    asset_id : str
        The ID of the asset being transferred
    note_type : str
        The type of note (private or public)
    memo : str, optional
        Optional memo for the note
    timestamp : int, optional
        The timestamp of the note creation (generated if not provided)
    
    Attributes
    ----------
    id : str
        The note ID
    sender : str
        The sender's account ID
    recipient : str
        The recipient's account ID
    amount : int
        The amount of the asset being transferred
    asset_id : str
        The ID of the asset being transferred
    note_type : str
        The type of note (private or public)
    memo : str
        Optional memo for the note
    timestamp : int
        The timestamp of the note creation
    """
    
    id: str = Field(default_factory=lambda: f"0x{uuid.uuid4().hex}")
    sender: str
    recipient: str
    amount: int
    asset_id: str
    note_type: str
    memo: str = ""
    timestamp: int = Field(default_factory=lambda: int(datetime.now().timestamp()))
    
    def __init__(self, **data):
        super().__init__(**data)
        # Validate addresses
        if not validate_address(self.sender):
            raise InvalidNoteError(f"Invalid sender address: {self.sender}")
        if not validate_address(self.recipient):
            raise InvalidNoteError(f"Invalid recipient address: {self.recipient}")
        # Validate amount
        if self.amount <= 0:
            raise InvalidNoteError(f"Invalid amount: {self.amount}")
        # Validate note type
        if self.note_type not in [NoteType.PRIVATE, NoteType.PUBLIC]:
            raise InvalidNoteError(f"Invalid note type: {self.note_type}")
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the note to a dictionary.
        
        Returns
        -------
        Dict[str, Any]
            Note as a dictionary
        """
        return self.dict()
    
    def save(self, file_path: str) -> None:
        """
        Save the note to a file.
        
        Parameters
        ----------
        file_path : str
            Path to save the note to
        """
        save_json(self.to_dict(), file_path)
    
    @classmethod
    def load(cls, file_path: str) -> 'Note':
        """
        Load a note from a file.
        
        Parameters
        ----------
        file_path : str
            Path to load the note from
            
        Returns
        -------
        Note
            Loaded note instance
            
        Raises
        ------
        FileNotFoundError
            If the file does not exist
        """
        data = load_json(file_path)
        return cls(**data)
    
    @classmethod
    def create(
        cls,
        sender: str,
        recipient: str,
        amount: int,
        asset_id: str,
        note_type: str = NoteType.PRIVATE,
        memo: str = ""
    ) -> 'Note':
        """
        Create a new note.
        
        Parameters
        ----------
        sender : str
            The sender's account ID
        recipient : str
            The recipient's account ID
        amount : int
            The amount of the asset being transferred
        asset_id : str
            The ID of the asset being transferred
        note_type : str, optional
            The type of note (private or public)
        memo : str, optional
            Optional memo for the note
            
        Returns
        -------
        Note
            A new note instance
        """
        return cls(
            sender=sender,
            recipient=recipient,
            amount=amount,
            asset_id=asset_id,
            note_type=note_type,
            memo=memo
        )
    
    @classmethod
    def import_note(cls, file_path: str) -> 'Note':
        """
        Import a note from a JSON file.
        
        This is an alias for Note.load() for a more intuitive API.
        
        Parameters
        ----------
        file_path : str
            Path to the note file
            
        Returns
        -------
        Note
            The imported note
        """
        return cls.load(file_path)
    
    def export_note(self, file_path: str) -> None:
        """
        Export a note to a JSON file.
        
        This is an alias for note.save() for a more intuitive API.
        
        Parameters
        ----------
        file_path : str
            Path to save the note to
        """
        self.save(file_path) 