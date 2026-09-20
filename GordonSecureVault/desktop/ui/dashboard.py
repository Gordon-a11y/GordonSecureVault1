"""
Dashboard Frame - Overview and statistics
"""

import customtkinter as ctk
from pathlib import Path
from core.vault.manager import VaultManager
from core.backup.backup_manager import BackupManager
import logging

logger = logging.getLogger(__name__)


class DashboardFrame(ctk.CTkFrame):
    """Dashboard overview frame"""
    
    title = "Dashboard"
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#000000")
        
        # Initialize managers
        self.vault_manager = VaultManager(str(controller.vaults_dir))
        self.backup_manager = BackupManager(str(controller.backups_dir))
        
        self._create_widgets()
        self._update_stats()
    
    def _create_widgets(self):
        """Create dashboard widgets"""
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="Dashboard Overview",
            font=("Arial", 28, "bold"),
            text_color="#C41E3A"
        )
        header.pack(pady=20, padx=20)
        
        # Stats container
        stats_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        stats_frame.pack(fill="both", padx=20, pady=10)
        
        # Stats grid
        stats_grid = ctk.CTkFrame(stats_frame, fg_color="#1a1a1a")
        stats_grid.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Stat cards
        self.vault_count_label = self._create_stat_card(
            stats_grid,
            "🔒 Total Vaults",
            "0",
            row=0, col=0
        )
        
        self.files_count_label = self._create_stat_card(
            stats_grid,
            "📁 Total Files",
            "0",
            row=0, col=1
        )
        
        self.storage_label = self._create_stat_card(
            stats_grid,
            "💾 Storage Used",
            "0 MB",
            row=0, col=2
        )
        
        self.backup_count_label = self._create_stat_card(
            stats_grid,
            "💾 Backups",
            "0",
            row=0, col=3
        )
        
        # Activities section
        activities_header = ctk.CTkLabel(
            self,
            text="Recent Activities",
            font=("Arial", 16, "bold"),
            text_color="#FFFFFF"
        )
        activities_header.pack(pady=(20, 10), padx=20)
        
        # Activities list
        self.activities_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        self.activities_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Refresh button
        refresh_btn = ctk.CTkButton(
            self,
            text="🔄 Refresh Statistics",
            font=("Arial", 12),
            fg_color="#C41E3A",
            command=self._update_stats
        )
        refresh_btn.pack(pady=20)
    
    def _create_stat_card(self, parent, label: str, value: str, row: int, col: int):
        """Create a stat card"""
        card = ctk.CTkFrame(parent, fg_color="#2a2a2a", corner_radius=10)
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        parent.grid_columnconfigure(col, weight=1)
        
        label_widget = ctk.CTkLabel(
            card,
            text=label,
            font=("Arial", 12),
            text_color="#999999"
        )
        label_widget.pack(pady=10)
        
        value_widget = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 24, "bold"),
            text_color="#C41E3A"
        )
        value_widget.pack(pady=10, padx=20)
        
        return value_widget
    
    def _update_stats(self):
        """Update statistics"""
        try:
            # Get vaults
            vaults = self.vault_manager.list_vaults()
            self.vault_count_label.configure(text=str(len(vaults)))
            
            # Get total files and storage
            total_files = 0
            total_storage = 0
            
            for vault in vaults:
                vault_name = vault["name"]
                files = self.vault_manager.get_vault_files(vault_name)
                total_files += len(files)
                
                vault_path = self.controller.vaults_dir / vault_name
                total_storage += self.vault_manager.get_vault_size(vault_name)
            
            self.files_count_label.configure(text=str(total_files))
            
            # Format storage
            if total_storage > 1024 * 1024 * 1024:  # GB
                storage_str = f"{total_storage / (1024**3):.2f} GB"
            elif total_storage > 1024 * 1024:  # MB
                storage_str = f"{total_storage / (1024**2):.2f} MB"
            else:  # KB
                storage_str = f"{total_storage / 1024:.2f} KB"
            
            self.storage_label.configure(text=storage_str)
            
            # Get backups
            backups = self.backup_manager.list_backups()
            self.backup_count_label.configure(text=str(len(backups)))
            
            # Update activities
            self._update_activities()
            
            logger.info("Dashboard statistics updated")
        except Exception as e:
            logger.error(f"Error updating statistics: {e}")
    
    def _update_activities(self):
        """Update activities list"""
        # Clear old widgets
        for widget in self.activities_frame.winfo_children():
            widget.destroy()
        
        # Show recent activities (placeholder)
        activity_labels = [
            "✓ Vault 'Personal' opened successfully",
            "✓ Backup created for 'Documents'",
            "✓ 3 files added to 'Work Vault'",
            "✓ Security check completed",
        ]
        
        for activity in activity_labels:
            activity_label = ctk.CTkLabel(
                self.activities_frame,
                text=activity,
                font=("Arial", 11),
                text_color="#CCCCCC",
                anchor="w"
            )
            activity_label.pack(fill="x", padx=10, pady=5)
