"""
Gordon Secure Vault - Backup Manager
Handle backup creation and restoration
"""

import json
import shutil
import zipfile
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import logging

from core.crypto.encryption import CryptographyEngine

logger = logging.getLogger(__name__)


class BackupManager:
    """Manage vault backups"""
    
    BACKUP_EXTENSION = ".gsbk"  # Gordon Secure Backup
    
    def __init__(self, backup_base_path: str):
        """
        Initialize backup manager
        
        Args:
            backup_base_path: Base directory for backups
        """
        self.backup_base_path = Path(backup_base_path)
        self.backup_base_path.mkdir(parents=True, exist_ok=True)
        logger.info(f"Backup manager initialized at {backup_base_path}")
    
    def create_backup(
        self,
        vault_name: str,
        vault_path: str,
        backup_name: Optional[str] = None
    ) -> Dict:
        """
        Create a backup of a vault
        
        Args:
            vault_name: Name of the vault
            vault_path: Path to the vault directory
            backup_name: Custom backup name (auto-generated if not provided)
            
        Returns:
            Status dictionary
        """
        try:
            vault_path = Path(vault_path)
            if not vault_path.exists():
                return {"success": False, "error": "Vault not found"}
            
            # Generate backup name
            if backup_name is None:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                backup_name = f"{vault_name}_backup_{timestamp}"
            
            backup_file = self.backup_base_path / f"{backup_name}{self.BACKUP_EXTENSION}"
            
            # Create zip backup
            with zipfile.ZipFile(backup_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for file_path in vault_path.rglob("*"):
                    if file_path.is_file():
                        arcname = file_path.relative_to(vault_path.parent)
                        zipf.write(file_path, arcname)
            
            # Create backup metadata
            backup_info = {
                "backup_name": backup_name,
                "vault_name": vault_name,
                "created_at": datetime.now().isoformat(),
                "backup_file": str(backup_file),
                "vault_size": self._get_directory_size(vault_path),
                "file_hash": self._compute_file_hash(backup_file)
            }
            
            logger.info(f"Backup created: {backup_name}")
            return {
                "success": True,
                "backup_name": backup_name,
                "backup_path": str(backup_file),
                "created_at": backup_info["created_at"],
                "vault_size": backup_info["vault_size"]
            }
        except Exception as e:
            logger.error(f"Error creating backup: {e}")
            return {"success": False, "error": str(e)}
    
    def restore_backup(
        self,
        backup_file: str,
        restore_path: str
    ) -> Dict:
        """
        Restore a vault from backup
        
        Args:
            backup_file: Path to backup file
            restore_path: Where to restore the vault
            
        Returns:
            Status dictionary
        """
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                return {"success": False, "error": "Backup file not found"}
            
            restore_dir = Path(restore_path)
            restore_dir.mkdir(parents=True, exist_ok=True)
            
            # Extract backup
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                zipf.extractall(restore_dir.parent)
            
            # Get vault name from restored directory
            restored_items = list(restore_dir.parent.glob("*"))
            vault_dir = None
            
            for item in restored_items:
                if item.is_dir() and item.name != restore_dir.name:
                    vault_dir = item
                    break
            
            if not vault_dir:
                return {"success": False, "error": "Invalid backup format"}
            
            # Verify backup integrity
            metadata_file = vault_dir / "metadata.json"
            if not metadata_file.exists():
                return {"success": False, "error": "Vault metadata not found in backup"}
            
            logger.info(f"Backup restored: {vault_dir.name}")
            return {
                "success": True,
                "vault_name": vault_dir.name,
                "restored_path": str(vault_dir)
            }
        except zipfile.BadZipFile:
            logger.error("Invalid backup file format")
            return {"success": False, "error": "Invalid backup file format"}
        except Exception as e:
            logger.error(f"Error restoring backup: {e}")
            return {"success": False, "error": str(e)}
    
    def list_backups(self, vault_name: Optional[str] = None) -> List[Dict]:
        """
        List available backups
        
        Args:
            vault_name: Filter by vault name (optional)
            
        Returns:
            List of backup info dictionaries
        """
        backups = []
        try:
            for backup_file in self.backup_base_path.glob(f"*{self.BACKUP_EXTENSION}"):
                backup_info = {
                    "backup_name": backup_file.stem,
                    "backup_path": str(backup_file),
                    "created_at": datetime.fromtimestamp(
                        backup_file.stat().st_mtime
                    ).isoformat(),
                    "size": backup_file.stat().st_size
                }
                
                if vault_name is None or vault_name in backup_file.name:
                    backups.append(backup_info)
            
            # Sort by creation time (newest first)
            backups.sort(key=lambda x: x["created_at"], reverse=True)
            logger.info(f"Found {len(backups)} backups")
            return backups
        except Exception as e:
            logger.error(f"Error listing backups: {e}")
            return []
    
    def delete_backup(self, backup_file: str) -> Dict:
        """
        Delete a backup file
        
        Args:
            backup_file: Path to backup file
            
        Returns:
            Status dictionary
        """
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                return {"success": False, "error": "Backup file not found"}
            
            backup_path.unlink()
            logger.info(f"Backup deleted: {backup_path.name}")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error deleting backup: {e}")
            return {"success": False, "error": str(e)}
    
    def verify_backup(self, backup_file: str) -> Dict:
        """
        Verify backup integrity
        
        Args:
            backup_file: Path to backup file
            
        Returns:
            Verification result
        """
        try:
            backup_path = Path(backup_file)
            if not backup_path.exists():
                return {"success": False, "error": "Backup file not found"}
            
            # Try to open and list files
            with zipfile.ZipFile(backup_path, 'r') as zipf:
                file_list = zipf.namelist()
                
                # Check for metadata
                has_metadata = any("metadata.json" in f for f in file_list)
                
                if not has_metadata:
                    return {"success": False, "error": "Backup missing metadata"}
            
            # Compute hash
            file_hash = self._compute_file_hash(backup_path)
            
            logger.info(f"Backup verified: {backup_path.name}")
            return {
                "success": True,
                "backup_name": backup_path.stem,
                "file_count": len(file_list),
                "file_hash": file_hash,
                "size": backup_path.stat().st_size
            }
        except zipfile.BadZipFile:
            logger.error("Invalid backup file format")
            return {"success": False, "error": "Invalid backup file format"}
        except Exception as e:
            logger.error(f"Error verifying backup: {e}")
            return {"success": False, "error": str(e)}
    
    @staticmethod
    def _get_directory_size(path: Path) -> int:
        """Calculate total directory size"""
        total_size = 0
        for file_path in path.rglob("*"):
            if file_path.is_file():
                total_size += file_path.stat().st_size
        return total_size
    
    @staticmethod
    def _compute_file_hash(file_path: Path) -> str:
        """Compute SHA-512 hash of a file"""
        return CryptographyEngine.compute_hash_sha512(
            file_path.read_bytes()
        )


class BackupScheduler:
    """Schedule automatic backups"""
    
    def __init__(self, backup_manager: BackupManager):
        self.backup_manager = backup_manager
        self.schedules = {}
    
    def add_schedule(
        self,
        vault_name: str,
        vault_path: str,
        interval_hours: int
    ) -> bool:
        """
        Add automatic backup schedule
        
        Args:
            vault_name: Name of the vault
            vault_path: Path to vault
            interval_hours: Backup interval in hours
            
        Returns:
            Success status
        """
        try:
            self.schedules[vault_name] = {
                "vault_path": vault_path,
                "interval_hours": interval_hours,
                "last_backup": None,
                "enabled": True
            }
            logger.info(f"Backup schedule added for {vault_name}")
            return True
        except Exception as e:
            logger.error(f"Error adding schedule: {e}")
            return False
    
    def remove_schedule(self, vault_name: str) -> bool:
        """Remove backup schedule"""
        try:
            if vault_name in self.schedules:
                del self.schedules[vault_name]
                logger.info(f"Backup schedule removed for {vault_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error removing schedule: {e}")
            return False
