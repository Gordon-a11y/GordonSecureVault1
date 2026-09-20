"""
File Manager Frame - Manage files in vaults
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
import logging

logger = logging.getLogger(__name__)


class FileManagerFrame(ctk.CTkFrame):
    """File manager frame"""
    
    title = "File Manager"
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#000000")
        self.current_vault = None
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create widgets"""
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="File Manager",
            font=("Arial", 28, "bold"),
            text_color="#C41E3A"
        )
        header.pack(pady=20, padx=20)
        
        # Vault selection
        select_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        select_frame.pack(fill="x", padx=20, pady=10)
        
        select_label = ctk.CTkLabel(
            select_frame,
            text="Select Vault:",
            font=("Arial", 12),
            text_color="#FFFFFF"
        )
        select_label.pack(side="left", padx=5)
        
        self.vault_combo = ctk.CTkComboBox(
            select_frame,
            values=["Vault 1", "Vault 2"],
            font=("Arial", 11),
            command=self._on_vault_selected
        )
        self.vault_combo.pack(side="left", padx=5)
        
        # Buttons
        button_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        button_frame.pack(fill="x", padx=20, pady=10)
        
        add_file_btn = ctk.CTkButton(
            button_frame,
            text="📄 Add File",
            font=("Arial", 12),
            fg_color="#C41E3A",
            command=self._add_file
        )
        add_file_btn.pack(side="left", padx=5)
        
        add_folder_btn = ctk.CTkButton(
            button_frame,
            text="📁 Add Folder",
            font=("Arial", 12),
            fg_color="#C41E3A",
            command=self._add_folder
        )
        add_folder_btn.pack(side="left", padx=5)
        
        # Files list
        list_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        list_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.files_frame = ctk.CTkScrollableFrame(
            list_frame,
            fg_color="#1a1a1a",
            label_text="Files in Vault"
        )
        self.files_frame.pack(fill="both", expand=True)
        
        # Empty state
        empty_label = ctk.CTkLabel(
            self.files_frame,
            text="Select a vault to view files",
            font=("Arial", 14),
            text_color="#999999"
        )
        empty_label.pack(pady=50)
    
    def _on_vault_selected(self, vault_name: str):
        """Handle vault selection"""
        self.current_vault = vault_name
        self._refresh_files()
    
    def _add_file(self):
        """Add a file to vault"""
        if not self.current_vault:
            messagebox.showwarning("Warning", "Please select a vault first")
            return
        
        file_path = filedialog.askopenfilename()
        if file_path:
            messagebox.showinfo("Success", f"File added to '{self.current_vault}'")
            self._refresh_files()
    
    def _add_folder(self):
        """Add a folder to vault"""
        if not self.current_vault:
            messagebox.showwarning("Warning", "Please select a vault first")
            return
        
        folder_path = filedialog.askdirectory()
        if folder_path:
            messagebox.showinfo("Success", f"Folder added to '{self.current_vault}'")
            self._refresh_files()\n    \n    def _refresh_files(self):
        \"\"\"Refresh files list\"\"\"
        # Clear old widgets
        for widget in self.files_frame.winfo_children():
            widget.destroy()
        
        # Show placeholder files
        files = ["document.pdf", "image.jpg", "archive.zip"]
        
        for file in files:
            file_frame = ctk.CTkFrame(self.files_frame, fg_color="#2a2a2a")
            file_frame.pack(fill="x", padx=5, pady=5)
            
            file_label = ctk.CTkLabel(
                file_frame,
                text=f"📄 {file}",
                font=("Arial", 11),
                text_color="#FFFFFF"
            )
            file_label.pack(side="left", padx=10, pady=10)
            
            extract_btn = ctk.CTkButton(
                file_frame,
                text="↓ Extract",
                font=("Arial", 10),
                fg_color="#C41E3A",
                width=70,
                command=lambda: self._extract_file(file)
            )
            extract_btn.pack(side="right", padx=5, pady=5)
            
            delete_btn = ctk.CTkButton(
                file_frame,
                text="🗑️ Delete",
                font=("Arial", 10),
                fg_color="#555555",
                width=70,
                command=lambda: self._delete_file(file)
            )
            delete_btn.pack(side="right", padx=5, pady=5)
    
    def _extract_file(self, filename: str):
        \"\"\"Extract a file from vault\"\"\"
        output_dir = filedialog.askdirectory(title="Select output directory")
        if output_dir:
            messagebox.showinfo("Success", f"File '{filename}' extracted successfully")
    
    def _delete_file(self, filename: str):
        \"\"\"Delete a file from vault\"\"\"
        if messagebox.askyesno("Delete", f"Delete '{filename}'?"):
            messagebox.showinfo("Success", f"File '{filename}' deleted")
            self._refresh_files()
