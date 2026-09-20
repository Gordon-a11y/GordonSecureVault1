"""
Vault Manager Frame - Create and manage vaults
"""

import customtkinter as ctk
from tkinter import simpledialog, messagebox
from core.vault.manager import VaultManager
from core.crypto.encryption import PasswordValidator
import logging

logger = logging.getLogger(__name__)


class VaultManagerFrame(ctk.CTkFrame):
    """Vault manager frame"""
    
    title = "Vault Manager"
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#000000")
        
        # Initialize manager
        self.vault_manager = VaultManager(str(controller.vaults_dir))
        
        self._create_widgets()
        self._refresh_vaults()
    
    def _create_widgets(self):
        """Create widgets"""
        
        # Header
        header_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        header_frame.pack(fill="x", padx=20, pady=20)
        
        header = ctk.CTkLabel(
            header_frame,
            text="Vault Manager",
            font=("Arial", 28, "bold"),
            text_color="#C41E3A"
        )
        header.pack(side="left")
        
        # Create new vault button
        create_btn = ctk.CTkButton(
            header_frame,
            text="➕ New Vault",
            font=("Arial", 12),
            fg_color="#C41E3A",
            command=self._create_new_vault
        )
        create_btn.pack(side="right")
        
        # Vaults list
        list_frame = ctk.CTkFrame(self, fg_color="#000000")
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Scrollable frame
        self.scrollable_frame = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="#1a1a1a",
            label_text="Your Vaults"
        )
        self.scrollable_frame.pack(fill="both", expand=True)
        
        self.vault_widgets = {}
    
    def _create_new_vault(self):
        """Create a new vault"""
        # Ask for vault name
        vault_name = simpledialog.askstring(
            "New Vault",
            "Enter vault name:"
        )
        
        if not vault_name:
            return
        
        # Ask for password
        password = simpledialog.askstring(
            "New Vault",
            "Enter vault password:",
            show="*"
        )
        
        if not password:
            return
        
        # Validate password
        validation = PasswordValidator.validate(password)
        if not validation["valid"]:
            feedback = "\\n".join(validation["feedback"])
            messagebox.showwarning(
                "Weak Password",
                f"Password is too weak. Recommendations:\\n{feedback}"
            )
            return
        
        # Create vault
        result = self.vault_manager.create_vault(vault_name, password)
        
        if result["success"]:
            messagebox.showinfo("Success", f"Vault '{vault_name}' created successfully")
            self._refresh_vaults()
            logger.info(f"Vault created: {vault_name}")
        else:
            messagebox.showerror("Error", f"Failed to create vault: {result['error']}")
            logger.error(f"Error creating vault: {result['error']}")
    
    def _refresh_vaults(self):
        """Refresh vault list"""
        # Clear old widgets
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        self.vault_widgets.clear()
        
        # Get vaults
        vaults = self.vault_manager.list_vaults()
        
        if not vaults:
            empty_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="No vaults yet. Create one to get started!",
                font=("Arial", 14),
                text_color="#999999"
            )
            empty_label.pack(pady=50)
            return
        
        # Create vault widgets
        for vault in vaults:
            self._create_vault_widget(vault)
    
    def _create_vault_widget(self, vault: dict):
        """Create a vault widget"""
        vault_frame = ctk.CTkFrame(
            self.scrollable_frame,
            fg_color="#2a2a2a",
            corner_radius=10
        )
        vault_frame.pack(fill="x", padx=5, pady=10)
        
        # Vault info
        info_frame = ctk.CTkFrame(vault_frame, fg_color="#2a2a2a")
        info_frame.pack(fill="x", padx=15, pady=15)
        
        # Vault name
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"🔒 {vault['name']}",
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF"
        )
        name_label.pack(anchor="w")
        
        # Vault details
        details_text = f"Created: {vault['created_at'][:10]} | Files: {vault['files_count']} | Size: {vault['total_size']} bytes"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            font=("Arial", 10),
            text_color="#999999"
        )
        details_label.pack(anchor="w", pady=(5, 0))
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(vault_frame, fg_color="#2a2a2a")
        buttons_frame.pack(fill="x", padx=15, pady=(0, 15))
        
        open_btn = ctk.CTkButton(
            buttons_frame,
            text="🔓 Open",
            font=("Arial", 11),
            fg_color="#C41E3A",
            width=80,
            command=lambda: self._open_vault(vault["name"])
        )
        open_btn.pack(side="left", padx=5)
        
        rename_btn = ctk.CTkButton(
            buttons_frame,
            text="✏️ Rename",
            font=("Arial", 11),
            fg_color="#333333",
            width=80,
            command=lambda: self._rename_vault(vault["name"])
        )
        rename_btn.pack(side="left", padx=5)
        
        delete_btn = ctk.CTkButton(
            buttons_frame,
            text="🗑️ Delete",
            font=("Arial", 11),
            fg_color="#555555",
            width=80,
            command=lambda: self._delete_vault(vault["name"])
        )
        delete_btn.pack(side="left", padx=5)
    
    def _open_vault(self, vault_name: str):
        """Open a vault"""
        logger.info(f"Opening vault: {vault_name}")
        messagebox.showinfo("Info", f"Vault '{vault_name}' opened")
    
    def _rename_vault(self, vault_name: str):
        """Rename a vault"""
        new_name = simpledialog.askstring(
            "Rename Vault",
            f"Enter new name for '{vault_name}':"
        )
        
        if not new_name or new_name == vault_name:
            return
        
        result = self.vault_manager.rename_vault(vault_name, new_name)
        
        if result["success"]:
            messagebox.showinfo("Success", f"Vault renamed to '{new_name}'")
            self._refresh_vaults()
        else:
            messagebox.showerror("Error", result["error"])
    
    def _delete_vault(self, vault_name: str):
        """Delete a vault"""
        if messagebox.askyesno(
            "Delete Vault",
            f"Are you sure you want to delete '{vault_name}'? This cannot be undone."
        ):
            result = self.vault_manager.delete_vault(vault_name)
            
            if result["success"]:
                messagebox.showinfo("Success", f"Vault '{vault_name}' deleted")
                self._refresh_vaults()
            else:
                messagebox.showerror("Error", result["error"])
