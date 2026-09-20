"""
Gordon Secure Vault - File Operations
Handle encryption/decryption of files within vaults
"""

import os
import uuid
from pathlib import Path
from typing import Dict, Optional, Tuple
import logging
import json

from core.crypto.encryption import CryptographyEngine
from core.vault.manager import FileEntry

logger = logging.getLogger(__name__)


class FileOperations:
    """Handle file operations within vaults"""
    
    CHUNK_SIZE = 1024 * 1024  # 1MB chunks for large files
    
    def __init__(self, vault_base_path: str):
        self.vault_base_path = Path(vault_base_path)
    
    def add_file_to_vault(
        self,
        vault_name: str,
        source_file: str,
        password: str,
        vault_password_salt: bytes
    ) -> Dict:
        """
        Encrypt and add a file to a vault
        
        Args:
            vault_name: Name of the vault
            source_file: Path to source file
            password: Vault password
            vault_password_salt: Salt for the vault
            
        Returns:
            Status dictionary with file info
        """
        try:
            source_path = Path(source_file)
            if not source_path.exists():
                return {"success": False, "error": "Source file not found"}
            
            # Read file
            with open(source_path, 'rb') as f:
                file_data = f.read()
            
            # Derive encryption key
            key, _ = CryptographyEngine.derive_key_argon2id(password, vault_password_salt)
            
            # Encrypt file
            ciphertext, iv, tag = CryptographyEngine.encrypt_file(file_data, key)
            
            # Compute hash for integrity
            file_hash = CryptographyEngine.compute_hash_sha512(file_data)
            
            # Generate encrypted filename
            encrypted_filename = f"{uuid.uuid4().hex}.enc"
            encrypted_path = self.vault_base_path / vault_name / "files" / encrypted_filename
            
            # Write encrypted file
            with open(encrypted_path, 'wb') as f:
                f.write(ciphertext)
            
            # Create file entry
            file_entry = FileEntry(
                original_filename=source_path.name,
                encrypted_filename=encrypted_filename,
                file_size=len(file_data),
                hash_value=file_hash,
                iv=iv.hex(),
                tag=tag.hex()
            )
            
            logger.info(f"File added to vault: {source_path.name}")
            
            return {
                "success": True,
                "original_name": source_path.name,
                "encrypted_name": encrypted_filename,
                "size": len(file_data),
                "added_at": file_entry.added_at
            }
        except Exception as e:
            logger.error(f"Error adding file to vault: {e}")
            return {"success": False, "error": str(e)}
    
    def extract_file_from_vault(
        self,
        vault_name: str,
        encrypted_filename: str,
        password: str,
        vault_password_salt: bytes,
        output_path: str
    ) -> Dict:
        """
        Extract and decrypt a file from vault
        
        Args:
            vault_name: Name of the vault
            encrypted_filename: Name of encrypted file in vault
            password: Vault password
            vault_password_salt: Salt for the vault
            output_path: Where to save decrypted file
            
        Returns:
            Status dictionary
        """
        try:
            # Get file index
            index_file = self.vault_base_path / vault_name / "files_index.json"
            with open(index_file, 'r') as f:
                index = json.load(f)
            
            # Find file entry
            file_entry = None
            for entry in index.get("files", []):
                if entry["encrypted_filename"] == encrypted_filename:
                    file_entry = entry
                    break
            
            if not file_entry:
                return {"success": False, "error": "File not found in vault"}
            
            # Read encrypted file
            encrypted_path = self.vault_base_path / vault_name / "files" / encrypted_filename
            with open(encrypted_path, 'rb') as f:
                ciphertext = f.read()
            
            # Derive key
            key, _ = CryptographyEngine.derive_key_argon2id(password, vault_password_salt)
            
            # Decrypt file
            iv = bytes.fromhex(file_entry["iv"])
            tag = bytes.fromhex(file_entry["tag"])
            
            plaintext = CryptographyEngine.decrypt_file(ciphertext, key, iv, tag)
            
            # Verify integrity
            computed_hash = CryptographyEngine.compute_hash_sha512(plaintext)
            if computed_hash != file_entry["hash_value"]:
                return {"success": False, "error": "File integrity check failed"}
            
            # Write decrypted file
            output_file = Path(output_path) / file_entry["original_filename"]
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_file, 'wb') as f:
                f.write(plaintext)
            
            logger.info(f"File extracted: {file_entry['original_filename']}")
            
            return {
                "success": True,
                "original_name": file_entry["original_filename"],
                "output_path": str(output_file),
                "size": len(plaintext)
            }
        except Exception as e:
            logger.error(f"Error extracting file: {e}")
            return {"success": False, "error": str(e)}
    
    def delete_file_from_vault(
        self,
        vault_name: str,
        encrypted_filename: str
    ) -> Dict:
        """
        Delete a file from vault
        
        Args:
            vault_name: Name of the vault
            encrypted_filename: Name of encrypted file
            
        Returns:
            Status dictionary
        """
        try:
            # Delete encrypted file
            encrypted_path = self.vault_base_path / vault_name / "files" / encrypted_filename
            if encrypted_path.exists():
                encrypted_path.unlink()
            
            # Update index
            index_file = self.vault_base_path / vault_name / "files_index.json"
            with open(index_file, 'r') as f:
                index = json.load(f)
            
            index["files"] = [
                f for f in index["files"]
                if f["encrypted_filename"] != encrypted_filename
            ]
            
            with open(index_file, 'w') as f:
                json.dump(index, f, indent=4)
            
            logger.info(f"File deleted from vault: {encrypted_filename}")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error deleting file: {e}")
            return {"success": False, "error": str(e)}
    
    def add_folder_to_vault(
        self,
        vault_name: str,
        source_folder: str,
        password: str,
        vault_password_salt: bytes
    ) -> Dict:
        """
        Add all files from a folder to vault
        
        Args:
            vault_name: Name of the vault
            source_folder: Path to source folder
            password: Vault password
            vault_password_salt: Salt for the vault
            
        Returns:
            Status dictionary with results
        """
        try:
            source_path = Path(source_folder)
            if not source_path.is_dir():
                return {"success": False, "error": "Source is not a directory"}
            
            results = {
                "success": True,
                "files_added": 0,
                "errors": [],
                "total_size": 0
            }
            
            # Add all files from folder
            for file_path in source_path.rglob("*"):
                if file_path.is_file():
                    result = self.add_file_to_vault(
                        vault_name,
                        str(file_path),
                        password,
                        vault_password_salt
                    )
                    
                    if result["success"]:
                        results["files_added"] += 1
                        results["total_size"] += result["size"]
                    else:
                        results["errors"].append({
                            "file": file_path.name,
                            "error": result["error"]
                        })
            
            logger.info(f"Added {results['files_added']} files to vault")
            return results
        except Exception as e:
            logger.error(f"Error adding folder: {e}")
            return {"success": False, "error": str(e)}
    
    def search_files(self, vault_name: str, query: str) -> list:
        """
        Search for files in vault by filename
        
        Args:
            vault_name: Name of the vault
            query: Search query
            
        Returns:
            List of matching file entries
        """
        try:
            index_file = self.vault_base_path / vault_name / "files_index.json"
            with open(index_file, 'r') as f:
                index = json.load(f)
            
            query_lower = query.lower()
            results = [
                f for f in index.get("files", [])
                if query_lower in f["original_filename"].lower()
            ]
            
            return results
        except Exception as e:
            logger.error(f"Error searching files: {e}")
            return []
