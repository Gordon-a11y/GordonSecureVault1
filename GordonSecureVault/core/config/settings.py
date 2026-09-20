"""
Gordon Secure Vault - Configuration Module
Manage application settings and preferences
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class ConfigManager:
    """Manage application configuration"""
    
    # Default settings
    DEFAULT_CONFIG = {
        "theme": {
            "mode": "dark",
            "primary_color": "#C41E3A",  # Crimson Red
            "background": "#000000",     # Black
            "text_color": "#FFFFFF",     # White
            "accent_color": "#333333"    # Dark Gray
        },
        "security": {
            "encryption_algorithm": "AES-256-GCM",
            "key_derivation": "Argon2id",
            "auto_lock_timeout": 600,  # seconds
            "require_password_on_startup": True,
            "enable_security_logs": True
        },
        "backup": {
            "auto_backup_enabled": False,
            "auto_backup_interval": 24,  # hours
            "backup_encryption": True,
            "keep_backups": 10
        },
        "language": "en",
        "window": {
            "width": 1200,
            "height": 700,
            "maximized": False
        },
        "vault_defaults": {
            "default_location": None,
            "auto_open_last_vault": False
        },
        "advanced": {
            "enable_logging": True,
            "log_level": "INFO",
            "chunk_size_mb": 1,
            "compression_enabled": True
        }
    }
    
    def __init__(self, config_path: str):
        """
        Initialize config manager
        
        Args:
            config_path: Path to config file
        """
        self.config_file = Path(config_path)
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self.config = self._load_config()
    
    def _load_config(self) -> Dict:
        """Load configuration from file"""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                logger.info("Configuration loaded from file")
                return config
            else:
                logger.info("Creating new configuration with defaults")
                self._save_config(self.DEFAULT_CONFIG)
                return self.DEFAULT_CONFIG.copy()
        except Exception as e:
            logger.error(f"Error loading config: {e}")
            return self.DEFAULT_CONFIG.copy()
    
    def _save_config(self, config: Dict = None) -> bool:
        """Save configuration to file"""
        try:
            if config is None:
                config = self.config
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            logger.info("Configuration saved")
            return True
        except Exception as e:
            logger.error(f"Error saving config: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key (supports dot notation: "section.key")
            default: Default value if key not found
            
        Returns:
            Configuration value
        """
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set configuration value
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
            
        Returns:
            Success status
        """
        try:
            keys = key.split('.')
            config = self.config
            
            # Navigate to the parent of the target key
            for k in keys[:-1]:
                if k not in config:
                    config[k] = {}
                config = config[k]
            
            # Set the value
            config[keys[-1]] = value
            self._save_config()
            return True
        except Exception as e:
            logger.error(f"Error setting config: {e}")
            return False
    
    def get_theme(self) -> Dict:
        """Get theme configuration"""
        return self.get("theme", {})
    
    def get_security_settings(self) -> Dict:
        """Get security settings"""
        return self.get("security", {})
    
    def get_backup_settings(self) -> Dict:
        """Get backup settings"""
        return self.get("backup", {})
    
    def reset_to_defaults(self) -> bool:
        """Reset configuration to defaults"""
        try:
            self.config = self.DEFAULT_CONFIG.copy()
            self._save_config()
            logger.info("Configuration reset to defaults")
            return True
        except Exception as e:
            logger.error(f"Error resetting config: {e}")
            return False
    
    def export_config(self, export_path: str) -> bool:
        """Export configuration to file"""
        try:
            export_file = Path(export_path)
            export_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_file, 'w') as f:
                json.dump(self.config, f, indent=4)
            
            logger.info(f"Configuration exported to {export_path}")
            return True
        except Exception as e:
            logger.error(f"Error exporting config: {e}")
            return False
    
    def import_config(self, import_path: str) -> bool:
        """Import configuration from file"""
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                logger.error("Import file not found")
                return False
            
            with open(import_file, 'r') as f:
                config = json.load(f)
            
            self.config = config
            self._save_config()
            logger.info(f"Configuration imported from {import_path}")
            return True
        except Exception as e:
            logger.error(f"Error importing config: {e}")
            return False


class ProfileManager:
    """Manage user profiles and preferences"""
    
    def __init__(self, profiles_path: str):
        """
        Initialize profile manager
        
        Args:
            profiles_path: Path to profiles directory
        """
        self.profiles_path = Path(profiles_path)
        self.profiles_path.mkdir(parents=True, exist_ok=True)
        self.current_profile = "default"
    
    def create_profile(self, profile_name: str) -> bool:
        """Create a new profile"""
        try:
            profile_dir = self.profiles_path / profile_name
            profile_dir.mkdir(exist_ok=False)
            logger.info(f"Profile created: {profile_name}")
            return True
        except FileExistsError:
            logger.error(f"Profile already exists: {profile_name}")
            return False
    
    def delete_profile(self, profile_name: str) -> bool:
        """Delete a profile"""
        try:
            if profile_name == "default":
                logger.error("Cannot delete default profile")
                return False
            
            profile_dir = self.profiles_path / profile_name
            if profile_dir.exists():
                import shutil
                shutil.rmtree(profile_dir)
                logger.info(f"Profile deleted: {profile_name}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting profile: {e}")
            return False
    
    def list_profiles(self) -> list:
        """List all profiles"""
        try:
            profiles = [d.name for d in self.profiles_path.iterdir() if d.is_dir()]
            return sorted(profiles)
        except Exception as e:
            logger.error(f"Error listing profiles: {e}")
            return ["default"]
    
    def set_current_profile(self, profile_name: str) -> bool:
        """Set current active profile"""
        try:
            profile_dir = self.profiles_path / profile_name
            if not profile_dir.exists():
                logger.error(f"Profile not found: {profile_name}")
                return False
            
            self.current_profile = profile_name
            logger.info(f"Profile switched to: {profile_name}")
            return True
        except Exception as e:
            logger.error(f"Error setting profile: {e}")
            return False
