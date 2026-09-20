"""
Gordon Secure Vault - Logging Module
Centralized logging with rotation and archiving
"""

import logging
import logging.handlers
from pathlib import Path
from datetime import datetime
import json


class LoggerSetup:
    """Setup and manage application logging"""
    
    # Log levels
    SECURITY = logging.WARNING
    VAULT = logging.INFO
    BACKUP = logging.INFO
    APPLICATION = logging.INFO
    
    @staticmethod
    def setup_logging(log_base_path: str) -> None:
        """
        Setup logging system with multiple log files
        
        Args:
            log_base_path: Base directory for log files
        """
        log_dir = Path(log_base_path)
        log_dir.mkdir(parents=True, exist_ok=True)
        
        # Configure root logger
        root_logger = logging.getLogger()
        root_logger.setLevel(logging.DEBUG)
        
        # Remove existing handlers
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        
        # Create formatters
        detailed_formatter = logging.Formatter(
            '[%(asctime)s] [%(name)s] [%(levelname)s] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        security_formatter = logging.Formatter(
            '[%(asctime)s] [SECURITY] %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # Security log handler
        security_log = log_dir / "security.log"
        security_handler = logging.handlers.RotatingFileHandler(
            security_log,
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=10
        )
        security_handler.setLevel(logging.WARNING)
        security_handler.setFormatter(security_formatter)
        root_logger.addHandler(security_handler)
        
        # Vault operations log handler
        vault_log = log_dir / "vault.log"
        vault_handler = logging.handlers.RotatingFileHandler(
            vault_log,
            maxBytes=10 * 1024 * 1024,
            backupCount=10
        )
        vault_handler.setLevel(logging.INFO)
        vault_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(vault_handler)
        
        # Backup operations log handler
        backup_log = log_dir / "backup.log"
        backup_handler = logging.handlers.RotatingFileHandler(
            backup_log,
            maxBytes=10 * 1024 * 1024,
            backupCount=10
        )
        backup_handler.setLevel(logging.INFO)
        backup_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(backup_handler)
        
        # Application log handler
        application_log = log_dir / "application.log"
        application_handler = logging.handlers.RotatingFileHandler(
            application_log,
            maxBytes=10 * 1024 * 1024,
            backupCount=10
        )
        application_handler.setLevel(logging.INFO)
        application_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(application_handler)
        
        # Console handler (for development/debugging)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(detailed_formatter)
        root_logger.addHandler(console_handler)
        
        root_logger.info("Logging system initialized")


class SecurityLogger:
    """Log security events"""
    
    def __init__(self):
        self.logger = logging.getLogger("security")
    
    def log_vault_opened(self, vault_name: str, user_ip: str = "localhost") -> None:
        """Log vault access"""
        self.logger.warning(
            f"Vault opened: {vault_name} from {user_ip}"
        )
    
    def log_vault_locked(self, vault_name: str) -> None:
        """Log vault lock"""
        self.logger.warning(f"Vault locked: {vault_name}")
    
    def log_failed_access_attempt(self, vault_name: str, reason: str) -> None:
        """Log failed access attempt"""
        self.logger.warning(
            f"Failed access attempt to {vault_name}: {reason}"
        )
    
    def log_key_operation(self, operation: str, vault_name: str) -> None:
        """Log key-related operations"""
        self.logger.warning(
            f"Key operation: {operation} on vault {vault_name}"
        )
    
    def log_backup_operation(self, operation: str, vault_name: str) -> None:
        """Log backup operations"""
        self.logger.warning(
            f"Backup operation: {operation} on vault {vault_name}"
        )


class OperationLogger:
    """Log general operations"""
    
    def __init__(self):
        self.logger = logging.getLogger("operations")
    
    def log_file_added(self, vault_name: str, filename: str, size: int) -> None:
        """Log file addition"""
        self.logger.info(
            f"File added to {vault_name}: {filename} ({size} bytes)"
        )
    
    def log_file_removed(self, vault_name: str, filename: str) -> None:
        """Log file removal"""
        self.logger.info(f"File removed from {vault_name}: {filename}")
    
    def log_file_extracted(self, vault_name: str, filename: str) -> None:
        """Log file extraction"""
        self.logger.info(f"File extracted from {vault_name}: {filename}")
    
    def log_vault_created(self, vault_name: str) -> None:
        """Log vault creation"""
        self.logger.info(f"Vault created: {vault_name}")
    
    def log_vault_deleted(self, vault_name: str) -> None:
        """Log vault deletion"""
        self.logger.info(f"Vault deleted: {vault_name}")


class ActivityMonitor:
    """Monitor and log user activities"""
    
    def __init__(self, log_base_path: str):
        self.log_dir = Path(log_base_path)
        self.activity_log = self.log_dir / "activity.json"
        self.activities = []
    
    def log_activity(self, activity_type: str, details: dict) -> None:
        """Log an activity"""
        activity = {
            "timestamp": datetime.now().isoformat(),
            "type": activity_type,
            "details": details
        }
        
        self.activities.append(activity)
        
        # Keep recent activities
        if len(self.activities) > 1000:
            self.activities = self.activities[-500:]
        
        # Save to file
        self._save_activities()
    
    def get_activities(
        self,
        activity_type: str = None,
        limit: int = 100
    ) -> list:
        """Get logged activities"""
        activities = self.activities
        
        if activity_type:
            activities = [
                a for a in activities
                if a["type"] == activity_type
            ]
        
        return activities[-limit:]
    
    def _save_activities(self) -> None:
        """Save activities to file"""
        try:
            with open(self.activity_log, 'w') as f:
                json.dump(self.activities, f, indent=2)
        except Exception as e:
            logging.error(f"Error saving activities: {e}")
    
    def load_activities(self) -> None:
        """Load activities from file"""
        try:
            if self.activity_log.exists():
                with open(self.activity_log, 'r') as f:
                    self.activities = json.load(f)
        except Exception as e:
            logging.error(f"Error loading activities: {e}")
