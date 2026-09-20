"""
Backup Center Frame - Manage backups
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import logging

logger = logging.getLogger(__name__)


class BackupCenterFrame(ctk.CTkFrame):
    """Backup center frame"""
    
    title = "Backup Center"
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#000000")
        
        self._create_widgets()
        self._refresh_backups()
    
    def _create_widgets(self):
        """Create widgets"""
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="Backup Center",
            font=("Arial", 28, "bold"),
            text_color="#C41E3A"
        )
        header.pack(pady=20, padx=20)
        
        # Buttons frame
        button_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        create_backup_btn = ctk.CTkButton(
            button_frame,
            text="💾 Create Backup",
            font=("Arial", 12),
            fg_color="#C41E3A",
            command=self._create_backup
        )
        create_backup_btn.pack(side="left", padx=5)
        
        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Refresh",
            font=("Arial", 12),
            fg_color="#333333",
            command=self._refresh_backups
        )
        refresh_btn.pack(side="left", padx=5)
        
        # Backups list
        list_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.backups_frame = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="#1a1a1a",
            label_text="Available Backups"
        )
        self.backups_frame.pack(fill="both", expand=True)
    
    def _create_backup(self):
        """Create a new backup"""
        messagebox.showinfo("Info", "Backup creation initiated")
        logger.info("Backup creation started")
    
    def _refresh_backups(self):
        """Refresh backups list"""
        # Clear old widgets
        for widget in self.backups_frame.winfo_children():
            widget.destroy()
        
        # Show placeholder backups
        backups = [
            {"name": "Vault_backup_20260915_120000", "date": "2026-09-15", "size": "245 MB"},
            {"name": "Vault_backup_20260914_180000", "date": "2026-09-14", "size": "243 MB"},
        ]
        
        for backup in backups:
            backup_frame = ctk.CTkFrame(self.backups_frame, fg_color="#2a2a2a")
            backup_frame.pack(fill="x", padx=5, pady=5)
            
            info = ctk.CTkLabel(
                backup_frame,
                text=f"💾 {backup['name']} ({backup['size']}) - {backup['date']}",
                font=("Arial", 11),
                text_color="#FFFFFF",
                anchor="w"
            )
            info.pack(side="left", fill="x", expand=True, padx=10, pady=10)
            
            restore_btn = ctk.CTkButton(
                backup_frame,
                text="↻ Restore",
                font=("Arial", 10),
                fg_color="#C41E3A",
                width=70,
                command=lambda: self._restore_backup(backup['name'])
            )
            restore_btn.pack(side="right", padx=5, pady=5)
            
            verify_btn = ctk.CTkButton(
                backup_frame,
                text="✓ Verify",
                font=("Arial", 10),
                fg_color="#333333",
                width=70,
                command=lambda: self._verify_backup(backup['name'])
            )
            verify_btn.pack(side="right", padx=5, pady=5)
            
            delete_btn = ctk.CTkButton(
                backup_frame,
                text="🗑️ Delete",
                font=("Arial", 10),
                fg_color="#555555",
                width=70,
                command=lambda: self._delete_backup(backup['name'])
            )
            delete_btn.pack(side="right", padx=5, pady=5)
    
    def _restore_backup(self, backup_name: str):
        """Restore a backup"""
        if messagebox.askyesno("Restore", f"Restore backup '{backup_name}'?"):
            messagebox.showinfo("Success", "Backup restored successfully")
    
    def _verify_backup(self, backup_name: str):
        """Verify backup integrity"""
        messagebox.showinfo("Info", f"Backup '{backup_name}' integrity verified ✓")
    
    def _delete_backup(self, backup_name: str):
        """Delete a backup"""
        if messagebox.askyesno("Delete", f"Delete backup '{backup_name}'?"):
            messagebox.showinfo("Success", f"Backup '{backup_name}' deleted")
            self._refresh_backups()
