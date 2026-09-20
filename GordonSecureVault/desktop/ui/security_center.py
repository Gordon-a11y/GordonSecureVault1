"""
Security Center Frame - Security monitoring and settings
"""

import customtkinter as ctk
from core.crypto.encryption import PasswordValidator
import logging

logger = logging.getLogger(__name__)


class SecurityCenterFrame(ctk.CTkFrame):
    """Security center frame"""
    
    title = "Security Center"
    
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(fg_color="#000000")
        
        self._create_widgets()
    
    def _create_widgets(self):
        """Create widgets"""
        
        # Header
        header = ctk.CTkLabel(
            self,
            text="Security Center",
            font=("Arial", 28, "bold"),
            text_color="#C41E3A"
        )
        header.pack(pady=20, padx=20)
        
        # Password strength checker
        self._create_password_checker()
        
        # Security stats
        self._create_security_stats()
        
        # Security settings
        self._create_security_settings()
    
    def _create_password_checker(self):
        """Create password strength checker"""
        checker_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        checker_frame.pack(fill="x", padx=20, pady=10)
        
        title = ctk.CTkLabel(
            checker_frame,
            text="Password Strength Checker",
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(anchor="w", padx=10, pady=(10, 5))
        
        input_frame = ctk.CTkFrame(checker_frame, fg_color="#1a1a1a")
        input_frame.pack(fill="x", padx=10, pady=5)
        
        password_label = ctk.CTkLabel(
            input_frame,
            text="Test Password:",
            font=("Arial", 11),
            text_color="#FFFFFF"
        )
        password_label.pack(side="left", padx=5)
        
        self.password_entry = ctk.CTkEntry(
            input_frame,
            font=("Arial", 11),
            show="*"
        )
        self.password_entry.pack(side="left", fill="x", expand=True, padx=5)
        
        check_btn = ctk.CTkButton(
            input_frame,
            text="Check Strength",
            font=("Arial", 11),
            fg_color="#C41E3A",
            command=self._check_password_strength
        )
        check_btn.pack(side="left", padx=5)
        
        # Result frame
        self.result_frame = ctk.CTkFrame(checker_frame, fg_color="#1a1a1a")
        self.result_frame.pack(fill="x", padx=10, pady=10)
    
    def _create_security_stats(self):
        """Create security statistics"""
        stats_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        stats_frame.pack(fill="x", padx=20, pady=10)
        
        title = ctk.CTkLabel(
            stats_frame,
            text="Security Statistics",
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Stats grid
        grid_frame = ctk.CTkFrame(stats_frame, fg_color="#1a1a1a")
        grid_frame.pack(fill="x", padx=10, pady=10)
        
        # Encryption status
        enc_frame = ctk.CTkFrame(grid_frame, fg_color="#2a2a2a", corner_radius=8)
        enc_frame.pack(fill="x", padx=5, pady=5)
        
        enc_label = ctk.CTkLabel(
            enc_frame,
            text="🔐 Encryption: AES-256-GCM",
            font=("Arial", 11),
            text_color="#C41E3A"
        )
        enc_label.pack(padx=10, pady=8)
        
        # Last login
        login_frame = ctk.CTkFrame(grid_frame, fg_color="#2a2a2a", corner_radius=8)
        login_frame.pack(fill="x", padx=5, pady=5)
        
        login_label = ctk.CTkLabel(
            login_frame,
            text="📅 Last Login: 2026-09-19 15:32:00",
            font=("Arial", 11),
            text_color="#FFFFFF"
        )
        login_label.pack(padx=10, pady=8)
        
        # Failed attempts
        fail_frame = ctk.CTkFrame(grid_frame, fg_color="#2a2a2a", corner_radius=8)
        fail_frame.pack(fill="x", padx=5, pady=5)
        
        fail_label = ctk.CTkLabel(
            fail_frame,
            text="⚠️ Failed Attempts: 0",
            font=("Arial", 11),
            text_color="#FFFFFF"
        )
        fail_label.pack(padx=10, pady=8)
    
    def _create_security_settings(self):
        """Create security settings"""
        settings_frame = ctk.CTkFrame(self, fg_color="#1a1a1a")
        settings_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        title = ctk.CTkLabel(
            settings_frame,
            text="Security Settings",
            font=("Arial", 14, "bold"),
            text_color="#FFFFFF"
        )
        title.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Settings list
        settings_list = ctk.CTkFrame(settings_frame, fg_color="#1a1a1a")
        settings_list.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Auto lock
        autolock_frame = ctk.CTkFrame(settings_list, fg_color="#2a2a2a", corner_radius=8)
        autolock_frame.pack(fill="x", padx=5, pady=5)
        
        autolock_label = ctk.CTkLabel(
            autolock_frame,
            text="Auto-lock timeout (minutes):",
            font=("Arial", 11),
            text_color="#FFFFFF"
        )
        autolock_label.pack(side="left", padx=10, pady=8)
        
        autolock_var = ctk.StringVar(value="10")
        autolock_spin = ctk.CTkComboBox(
            autolock_frame,
            values=["5", "10", "15", "30", "60"],
            variable=autolock_var,
            font=("Arial", 10),
            width=100
        )
        autolock_spin.pack(side="right", padx=10, pady=8)
        
        # Two-factor auth
        twofa_frame = ctk.CTkFrame(settings_list, fg_color="#2a2a2a", corner_radius=8)
        twofa_frame.pack(fill="x", padx=5, pady=5)
        
        twofa_label = ctk.CTkLabel(
            twofa_frame,
            text="Two-Factor Authentication:",
            font=("Arial", 11),
            text_color="#FFFFFF"
        )
        twofa_label.pack(side="left", padx=10, pady=8)
        
        twofa_switch = ctk.CTkSwitch(
            twofa_frame,
            text="",
            fg_color="#C41E3A"
        )
        twofa_switch.pack(side="right", padx=10, pady=8)
    
    def _check_password_strength(self):
        """Check password strength"""
        password = self.password_entry.get()
        
        # Clear old result
        for widget in self.result_frame.winfo_children():
            widget.destroy()
        
        if not password:
            return
        
        # Validate password
        result = PasswordValidator.validate(password)
        
        # Color based on score
        if result["score"] >= 75:
            color = "#00FF00"
            strength = "Strong"
        elif result["score"] >= 50:
            color = "#FFFF00"
            strength = "Moderate"
        else:
            color = "#FF0000"
            strength = "Weak"
        
        # Display result
        strength_label = ctk.CTkLabel(
            self.result_frame,
            text=f"Strength: {strength} ({result['score']}/100)",
            font=("Arial", 12, "bold"),
            text_color=color
        )
        strength_label.pack(pady=5)
        
        # Feedback
        if result["feedback"]:
            feedback_text = "Recommendations:\\n" + "\\n".join(f"• {f}" for f in result["feedback"])
            feedback_label = ctk.CTkLabel(
                self.result_frame,
                text=feedback_text,
                font=("Arial", 10),
                text_color="#CCCCCC",
                justify="left"
            )
            feedback_label.pack(pady=5)
