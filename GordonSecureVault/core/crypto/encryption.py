"""
Gordon Secure Vault - Cryptography Module
Implements AES-256-GCM encryption with Argon2id key derivation
"""

import os
import hashlib
from typing import Tuple
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.argon2id import Argon2id
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives import hashes
import logging

logger = logging.getLogger(__name__)


class CryptographyEngine:
    """Secure encryption/decryption engine using AES-256-GCM"""

    # Constants
    KEY_SIZE = 32  # 256-bit
    SALT_SIZE = 32  # 256-bit salt
    IV_SIZE = 12  # 96-bit IV for GCM
    TAG_SIZE = 16  # 128-bit authentication tag
    
    # Argon2id parameters
    ARGON2_TIME_COST = 3
    ARGON2_MEMORY_COST = 65536  # 64MB
    ARGON2_PARALLELISM = 4

    @staticmethod
    def generate_random_bytes(size: int) -> bytes:
        """Generate cryptographically secure random bytes"""
        return os.urandom(size)

    @classmethod
    def derive_key_argon2id(
        cls,
        password: str,
        salt: bytes = None
    ) -> Tuple[bytes, bytes]:
        """
        Derive encryption key using Argon2id
        
        Args:
            password: User password
            salt: Salt for key derivation (generated if not provided)
            
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = cls.generate_random_bytes(cls.SALT_SIZE)
        
        try:
            kdf = Argon2id(
                time_cost=cls.ARGON2_TIME_COST,
                memory_cost=cls.ARGON2_MEMORY_COST,
                parallelism=cls.ARGON2_PARALLELISM
            )
            key = kdf.derive(password.encode())
            logger.info("Successfully derived key using Argon2id")
            return key[:cls.KEY_SIZE], salt
        except Exception as e:
            logger.error(f"Error deriving key with Argon2id: {e}")
            raise

    @classmethod
    def derive_key_pbkdf2(
        cls,
        password: str,
        salt: bytes = None,
        iterations: int = 480000
    ) -> Tuple[bytes, bytes]:
        """
        Derive encryption key using PBKDF2-HMAC-SHA512 (backup method)
        
        Args:
            password: User password
            salt: Salt for key derivation (generated if not provided)
            iterations: Number of iterations
            
        Returns:
            Tuple of (key, salt)
        """
        if salt is None:
            salt = cls.generate_random_bytes(cls.SALT_SIZE)
        
        try:
            kdf = PBKDF2(
                algorithm=hashes.SHA512(),
                length=cls.KEY_SIZE,
                salt=salt,
                iterations=iterations
            )
            key = kdf.derive(password.encode())
            logger.info("Successfully derived key using PBKDF2")
            return key, salt
        except Exception as e:
            logger.error(f"Error deriving key with PBKDF2: {e}")
            raise

    @staticmethod
    def encrypt_file(
        file_data: bytes,
        key: bytes,
        iv: bytes = None
    ) -> Tuple[bytes, bytes, bytes]:
        """
        Encrypt file data using AES-256-GCM
        
        Args:
            file_data: File content to encrypt
            key: Encryption key (32 bytes)
            iv: Initialization vector (generated if not provided)
            
        Returns:
            Tuple of (ciphertext, iv, tag)
        """
        if iv is None:
            iv = CryptographyEngine.generate_random_bytes(CryptographyEngine.IV_SIZE)
        
        if len(key) != CryptographyEngine.KEY_SIZE:
            raise ValueError(f"Key must be {CryptographyEngine.KEY_SIZE} bytes")
        
        if len(iv) != CryptographyEngine.IV_SIZE:
            raise ValueError(f"IV must be {CryptographyEngine.IV_SIZE} bytes")
        
        try:
            cipher = AESGCM(key)
            ciphertext = cipher.encrypt(iv, file_data, None)
            
            # Extract tag (last 16 bytes) from ciphertext
            tag = ciphertext[-CryptographyEngine.TAG_SIZE:]
            actual_ciphertext = ciphertext[:-CryptographyEngine.TAG_SIZE]
            
            logger.info(f"File encrypted successfully, size: {len(file_data)} bytes")
            return actual_ciphertext, iv, tag
        except Exception as e:
            logger.error(f"Error encrypting file: {e}")
            raise

    @staticmethod
    def decrypt_file(
        ciphertext: bytes,
        key: bytes,
        iv: bytes,
        tag: bytes
    ) -> bytes:
        """
        Decrypt file data using AES-256-GCM
        
        Args:
            ciphertext: Encrypted data
            key: Decryption key (32 bytes)
            iv: Initialization vector
            tag: Authentication tag
            
        Returns:
            Decrypted file data
        """
        if len(key) != CryptographyEngine.KEY_SIZE:
            raise ValueError(f"Key must be {CryptographyEngine.KEY_SIZE} bytes")
        
        if len(iv) != CryptographyEngine.IV_SIZE:
            raise ValueError(f"IV must be {CryptographyEngine.IV_SIZE} bytes")
        
        if len(tag) != CryptographyEngine.TAG_SIZE:
            raise ValueError(f"Tag must be {CryptographyEngine.TAG_SIZE} bytes")
        
        try:
            cipher = AESGCM(key)
            plaintext = cipher.decrypt(iv, ciphertext + tag, None)
            logger.info(f"File decrypted successfully, size: {len(plaintext)} bytes")
            return plaintext
        except Exception as e:
            logger.error(f"Error decrypting file: {e}")
            raise

    @staticmethod
    def compute_hash_sha512(data: bytes) -> str:
        """Compute SHA-512 hash for integrity verification"""
        return hashlib.sha512(data).hexdigest()

    @staticmethod
    def verify_hash(data: bytes, expected_hash: str) -> bool:
        """Verify data integrity using SHA-512"""
        computed_hash = CryptographyEngine.compute_hash_sha512(data)
        return computed_hash == expected_hash


class PasswordValidator:
    """Validate password strength"""
    
    @staticmethod
    def validate(password: str) -> dict:
        """
        Validate password strength
        
        Returns:
            dict with 'valid' boolean and 'score' (0-100)
        """
        score = 0
        feedback = []
        
        if len(password) < 8:
            feedback.append("Password must be at least 8 characters")
        else:
            score += 20
        
        if len(password) >= 12:
            score += 10
        
        if any(c.isupper() for c in password):
            score += 15
        else:
            feedback.append("Add uppercase letters")
        
        if any(c.islower() for c in password):
            score += 15
        else:
            feedback.append("Add lowercase letters")
        
        if any(c.isdigit() for c in password):
            score += 15
        else:
            feedback.append("Add numbers")
        
        if any(c in "!@#$%^&*()-_=+[]{}|;:,.<>?" for c in password):
            score += 25
        else:
            feedback.append("Add special characters")
        
        return {
            "valid": score >= 50,
            "score": min(score, 100),
            "feedback": feedback
        }
