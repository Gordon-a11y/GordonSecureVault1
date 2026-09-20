"""
Gordon Secure Vault - Vault Manager
Manages vault creation, operations, and structure
"""

import json
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional
import logging
from core.crypto.encryption import CryptographyEngine

logger = logging.getLogger(__name__)


class VaultMetadata:
    """Metadata for a vault"""
    
    def __init__(self, name: str, salt: bytes, created_at: str = None):
        self.name = name
        self.salt = salt.hex() if isinstance(salt, bytes) else salt
        self.created_at = created_at or datetime.now().isoformat()
        self.last_opened = None
        self.version = "1.0"
        self.files_count = 0
        self.total_size = 0
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "name": self.name,
            "salt": self.salt,
            "created_at": self.created_at,
            "last_opened": self.last_opened,
            "version": self.version,
            "files_count": self.files_count,
            "total_size": self.total_size
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'VaultMetadata':
        """Create from dictionary"""
        metadata = VaultMetadata(data["name"], bytes.fromhex(data["salt"]))
        metadata.created_at = data.get("created_at", metadata.created_at)
        metadata.last_opened = data.get("last_opened")
        metadata.version = data.get("version", "1.0")
        metadata.files_count = data.get("files_count", 0)
        metadata.total_size = data.get("total_size", 0)
        return metadata


class FileEntry:
    """Represents an encrypted file entry in a vault"""
    
    def __init__(
        self,
        original_filename: str,
        encrypted_filename: str,
        file_size: int,
        hash_value: str,
        iv: str,
        tag: str,
        added_at: str = None
    ):
        self.original_filename = original_filename
        self.encrypted_filename = encrypted_filename
        self.file_size = file_size
        self.hash_value = hash_value
        self.iv = iv
        self.tag = tag
        self.added_at = added_at or datetime.now().isoformat()
    
    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "original_filename": self.original_filename,
            "encrypted_filename": self.encrypted_filename,
            "file_size": self.file_size,
            "hash_value": self.hash_value,
            "iv": self.iv,
            "tag": self.tag,
            "added_at": self.added_at
        }
    
    @staticmethod
    def from_dict(data: dict) -> 'FileEntry':
        """Create from dictionary"""
        return FileEntry(
            data["original_filename"],
            data["encrypted_filename"],
            data["file_size"],
            data["hash_value"],
            data["iv"],
            data["tag"],
            data.get("added_at")
        )


class VaultManager:
    """Manage encrypted vaults"""
    
    VAULT_EXTENSION = ".gsv"  # Gordon Secure Vault
    METADATA_FILE = "metadata.json"
    FILES_INDEX = "files_index.json"
    
    def __init__(self, vault_base_path: str):
        """
        Initialize vault manager
        
        Args:
            vault_base_path: Base directory for all vaults
        """
        self.vault_base_path = Path(vault_base_path)
        self.vault_base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Vault manager initialized at {vault_base_path}")
    
    def create_vault(
        self,
        vault_name: str,
        password: str
    ) -> Dict:
        """
        Create a new encrypted vault
        
        Args:
            vault_name: Name of the vault
            password: User password
            
        Returns:
            Dictionary with vault info
        """
        try:
            # Generate salt and derive key
            salt = CryptographyEngine.generate_random_bytes(
                CryptographyEngine.SALT_SIZE
            )
            key, _ = CryptographyEngine.derive_key_argon2id(password, salt)
            
            # Create vault directory
            vault_dir = self.vault_base_path / vault_name
            vault_dir.mkdir(exist_ok=False)
            
            # Create files directory
            files_dir = vault_dir / "files"
            files_dir.mkdir()
            
            # Create metadata
            metadata = VaultMetadata(vault_name, salt)
            metadata_file = vault_dir / self.METADATA_FILE
            
            with open(metadata_file, 'w') as f:
                json.dump(metadata.to_dict(), f, indent=4)
            
            # Create empty files index
            index_file = vault_dir / self.FILES_INDEX
            with open(index_file, 'w') as f:
                json.dump({"files": []}, f, indent=4)
            
            logger.info(f"Vault '{vault_name}' created successfully")
            
            return {
                "success": True,
                "vault_name": vault_name,
                "path": str(vault_dir),
                "created_at": metadata.created_at
            }
        except FileExistsError:
            logger.error(f"Vault '{vault_name}' already exists")
            return {"success": False, "error": "Vault already exists"}
        except Exception as e:
            logger.error(f"Error creating vault: {e}")
            return {"success": False, "error": str(e)}
    
    def delete_vault(self, vault_name: str) -> Dict:
        """
        Delete a vault and all its contents
        
        Args:
            vault_name: Name of the vault
            
        Returns:
            Status dictionary
        """
        try:
            vault_dir = self.vault_base_path / vault_name
            if not vault_dir.exists():
                return {"success": False, "error": "Vault not found"}
            
            shutil.rmtree(vault_dir)
            logger.info(f"Vault '{vault_name}' deleted")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error deleting vault: {e}")
            return {"success": False, "error": str(e)}
    
    def list_vaults(self) -> List[Dict]:
        """
        List all available vaults
        
        Returns:
            List of vault metadata dictionaries
        """
        vaults = []
        try:
            for vault_dir in self.vault_base_path.iterdir():
                if vault_dir.is_dir():
                    metadata_file = vault_dir / self.METADATA_FILE
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)
                            vaults.append(metadata)
            logger.info(f"Found {len(vaults)} vaults")
            return vaults
        except Exception as e:
            logger.error(f"Error listing vaults: {e}")
            return []
    
    def get_vault_metadata(self, vault_name: str) -> Optional[Dict]:
        """Get metadata for a specific vault"""
        try:
            metadata_file = self.vault_base_path / vault_name / self.METADATA_FILE
            if not metadata_file.exists():
                return None
            
            with open(metadata_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error reading vault metadata: {e}")
            return None
    
    def rename_vault(self, old_name: str, new_name: str) -> Dict:
        """
        Rename a vault
        
        Args:
            old_name: Current vault name
            new_name: New vault name
            
        Returns:
            Status dictionary
        """
        try:
            old_dir = self.vault_base_path / old_name
            new_dir = self.vault_base_path / new_name
            
            if not old_dir.exists():
                return {"success": False, "error": "Vault not found"}
            
            if new_dir.exists():
                return {"success": False, "error": "New name already exists"}
            
            old_dir.rename(new_dir)
            
            # Update metadata
            metadata_file = new_dir / self.METADATA_FILE
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            metadata["name"] = new_name
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            logger.info(f"Vault renamed from '{old_name}' to '{new_name}'")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error renaming vault: {e}")
            return {"success": False, "error": str(e)}
    
    def update_last_opened(self, vault_name: str) -> bool:
        """Update last opened timestamp"""
        try:
            metadata_file = self.vault_base_path / vault_name / self.METADATA_FILE
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            metadata["last_opened"] = datetime.now().isoformat()
            
            with open(metadata_file, 'w') as f:
                json.dump(metadata, f, indent=4)
            
            return True
        except Exception as e:
            logger.error(f"Error updating last opened: {e}")
            return False
    
    def add_file_entry(self, vault_name: str, file_entry: FileEntry) -> bool:
        """Add file entry to index"""
        try:
            index_file = self.vault_base_path / vault_name / self.FILES_INDEX
            with open(index_file, 'r') as f:
                index = json.load(f)
            
            index["files"].append(file_entry.to_dict())
            
            with open(index_file, 'w') as f:
                json.dump(index, f, indent=4)
            
            return True
        except Exception as e:
            logger.error(f"Error adding file entry: {e}")
            return False
    
    def get_vault_files(self, vault_name: str) -> List[Dict]:
        """Get all files in a vault"""
        try:
            index_file = self.vault_base_path / vault_name / self.FILES_INDEX
            with open(index_file, 'r') as f:
                index = json.load(f)
            return index.get("files", [])
        except Exception as e:
            logger.error(f"Error getting vault files: {e}")
            return []
    
    def get_vault_size(self, vault_name: str) -> int:
        """Calculate total size of a vault"""
        try:
            files_dir = self.vault_base_path / vault_name / "files"
            total_size = 0
            
            for file in files_dir.rglob("*"):
                if file.is_file():
                    total_size += file.stat().st_size
            
            return total_size
        except Exception as e:
            logger.error(f"Error calculating vault size: {e}")
            return 0
