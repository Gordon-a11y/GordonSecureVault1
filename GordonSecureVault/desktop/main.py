"""
Gordon Secure Vault - Desktop Application
Windows UI using CustomTkinter
"""

import customtkinter as ctk
from pathlib import Path
import sys
import os

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from desktop.ui.dashboard import DashboardFrame
from desktop.ui.vault_manager import VaultManagerFrame
from desktop.ui.file_manager import FileManagerFrame
from desktop.ui.backup_center import BackupCenterFrame
from desktop.ui.security_center import SecurityCenterFrame
from core.logs.logger import LoggerSetup
from core.config.settings import ConfigManager
import logging

logger = logging.getLogger(__name__)


class MainApplication(ctk.CTk):
    """Main application window"""
    
    # Color scheme
    BG_COLOR = "#000000"        # Black
    ACCENT_COLOR = "#333333"    # Dark Gray
    PRIMARY_COLOR = "#C41E3A"   # Crimson Red
    TEXT_COLOR = "#FFFFFF"      # White
    
    def __init__(self):
        super().__init__()
        
        # Setup logging
        log_dir = Path.home() / ".gordon_secure_vault" / "logs"
        LoggerSetup.setup_logging(str(log_dir))
        logger.info("="*50)
        logger.info("Gordon Secure Vault - Desktop Application Started")
        logger.info("="*50)
        
        # Setup configuration
        config_file = Path.home() / ".gordon_secure_vault" / "config.json"
        self.config = ConfigManager(str(config_file))
        
        # Setup data directories
        self.app_data_dir = Path.home() / ".gordon_secure_vault"
        self.vaults_dir = self.app_data_dir / "vaults"
        self.backups_dir = self.app_data_dir / "backups"
        
        self.vaults_dir.mkdir(parents=True, exist_ok=True)
        self.backups_dir.mkdir(parents=True, exist_ok=True)
        
        # Window configuration
        self.title("Gordon Secure Vault")
        self.geometry("1200x700")
        self.minsize(1000, 600)
        
        # Set appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Configure colors
        self.configure(fg_color=self.BG_COLOR)
        
        # Create UI
        self._create_ui()
        
        logger.info("Application UI created successfully")
    
    def _create_ui(self):
        """Create main UI"""
        
        # Top navigation bar
        self._create_top_nav()
        
        # Main container
        self.main_container = ctk.CTkFrame(
            self,
            fg_color=self.BG_COLOR
        )
        self.main_container.grid(row=1, column=0, sticky="nsew", padx=0, pady=0)
        self.main_container.grid_columnconfigure(0, weight=0)
        self.main_container.grid_columnconfigure(1, weight=1)
        self.main_container.grid_rowconfigure(0, weight=1)
        
        # Sidebar
        self._create_sidebar()
        
        # Content area
        self.content_frame = ctk.CTkFrame(
            self.main_container,
            fg_color=self.BG_COLOR
        )
        self.content_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        # Frames dictionary
        self.frames = {}
        
        # Create all frames
        for F in (DashboardFrame, VaultManagerFrame, FileManagerFrame, 
                  BackupCenterFrame, SecurityCenterFrame):
            frame = F(self.content_frame, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show dashboard initially
        self.show_frame(DashboardFrame)
        
        # Configure grid
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
    
    def _create_top_nav(self):
        """Create top navigation bar"""
        top_frame = ctk.CTkFrame(self, fg_color=self.ACCENT_COLOR, height=60)
        top_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        top_frame.grid_columnconfigure(0, weight=1)
        
        # Title
        title = ctk.CTkLabel(
            top_frame,
            text="🔐 Gordon Secure Vault",
            font=("Arial", 20, "bold"),
            text_color=self.PRIMARY_COLOR
        )
        title.pack(side="left", padx=20, pady=10)
        
        # Info label
        self.info_label = ctk.CTkLabel(
            top_frame,
            text="Dashboard",
            font=("Arial", 14),
            text_color=self.TEXT_COLOR
        )
        self.info_label.pack(side="right", padx=20, pady=10)
    
    def _create_sidebar(self):
        """Create sidebar navigation"""
        sidebar = ctk.CTkFrame(
            self.main_container,
            fg_color=self.ACCENT_COLOR,
            width=200
        )
        sidebar.grid(row=0, column=0, sticky="ns", padx=0, pady=0)
        sidebar.grid_rowconfigure(5, weight=1)
        
        # Menu items
        menu_items = [
            ("📊 Dashboard", DashboardFrame),
            ("🔒 Vault Manager", VaultManagerFrame),
            ("📁 File Manager", FileManagerFrame),
            ("💾 Backup Center", BackupCenterFrame),
            ("🛡️ Security Center", SecurityCenterFrame),
        ]
        
        for i, (label, frame_class) in enumerate(menu_items):
            btn = ctk.CTkButton(
                sidebar,
                text=label,
                font=("Arial", 12),
                fg_color=self.ACCENT_COLOR,
                hover_color=self.PRIMARY_COLOR,
                text_color=self.TEXT_COLOR,
                command=lambda f=frame_class: self.show_frame(f)
            )
            btn.grid(row=i, column=0, sticky="ew", padx=10, pady=5)
        
        # Exit button at bottom
        exit_btn = ctk.CTkButton(
            sidebar,
            text="❌ Exit",
            font=("Arial", 12),
            fg_color=self.PRIMARY_COLOR,
            text_color=self.TEXT_COLOR,
            command=self.quit
        )
        exit_btn.grid(row=6, column=0, sticky="ew", padx=10, pady=10)
    
    def show_frame(self, cont):
        """Show a frame"""
        frame = self.frames[cont]
        frame.tkraise()
        self.info_label.configure(text=frame.title)
        logger.info(f"Switched to {frame.title}")


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
