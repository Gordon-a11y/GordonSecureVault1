"""
Unit tests for encryption module
"""

import pytest
from core.crypto.encryption import CryptographyEngine, PasswordValidator


class TestCryptographyEngine:
    """Test cryptographic operations"""
    
    def test_generate_random_bytes(self):
        """Test random byte generation"""
        size = 32
        random_bytes = CryptographyEngine.generate_random_bytes(size)
        
        assert len(random_bytes) == size
        assert isinstance(random_bytes, bytes)
        
        # Ensure bytes are random (different each time)
        random_bytes2 = CryptographyEngine.generate_random_bytes(size)
        assert random_bytes != random_bytes2
    
    def test_derive_key_argon2id(self):
        """Test Argon2id key derivation"""
        password = "TestPassword123!"
        
        key1, salt1 = CryptographyEngine.derive_key_argon2id(password)
        key2, salt2 = CryptographyEngine.derive_key_argon2id(password)
        
        # Same password should produce different keys with different salts
        assert key1 != key2
        assert salt1 != salt2
        assert len(key1) == CryptographyEngine.KEY_SIZE
        assert len(salt1) == CryptographyEngine.SALT_SIZE
    
    def test_derive_key_argon2id_with_salt(self):
        """Test Argon2id with provided salt"""
        password = "TestPassword123!"
        salt = CryptographyEngine.generate_random_bytes(CryptographyEngine.SALT_SIZE)
        
        key1, returned_salt = CryptographyEngine.derive_key_argon2id(password, salt)
        key2, _ = CryptographyEngine.derive_key_argon2id(password, salt)
        
        # Same password and salt should produce same key
        assert key1 == key2
        assert returned_salt == salt
    
    def test_derive_key_pbkdf2(self):
        """Test PBKDF2 key derivation"""
        password = "TestPassword123!"
        
        key1, salt1 = CryptographyEngine.derive_key_pbkdf2(password)
        key2, salt2 = CryptographyEngine.derive_key_pbkdf2(password)
        
        # Same password should produce different keys with different salts
        assert key1 != key2
        assert salt1 != salt2
        assert len(key1) == CryptographyEngine.KEY_SIZE
        assert len(salt1) == CryptographyEngine.SALT_SIZE
    
    def test_encrypt_decrypt_file(self):
        """Test file encryption and decryption"""
        original_data = b"This is a test file content"
        key = CryptographyEngine.generate_random_bytes(CryptographyEngine.KEY_SIZE)
        
        # Encrypt
        ciphertext, iv, tag = CryptographyEngine.encrypt_file(original_data, key)
        
        assert ciphertext != original_data
        assert len(iv) == CryptographyEngine.IV_SIZE
        assert len(tag) == CryptographyEngine.TAG_SIZE
        
        # Decrypt
        decrypted_data = CryptographyEngine.decrypt_file(ciphertext, key, iv, tag)
        
        assert decrypted_data == original_data
    
    def test_encrypt_file_different_ivs(self):
        """Test that each encryption uses different IV"""
        original_data = b"Test data"
        key = CryptographyEngine.generate_random_bytes(CryptographyEngine.KEY_SIZE)
        
        ciphertext1, iv1, _ = CryptographyEngine.encrypt_file(original_data, key)
        ciphertext2, iv2, _ = CryptographyEngine.encrypt_file(original_data, key)
        
        # Different IVs
        assert iv1 != iv2
        # Different ciphertexts
        assert ciphertext1 != ciphertext2
    
    def test_decrypt_with_wrong_key(self):
        """Test that decryption fails with wrong key"""
        original_data = b"Sensitive data"
        key1 = CryptographyEngine.generate_random_bytes(CryptographyEngine.KEY_SIZE)
        key2 = CryptographyEngine.generate_random_bytes(CryptographyEngine.KEY_SIZE)
        
        ciphertext, iv, tag = CryptographyEngine.encrypt_file(original_data, key1)
        
        # Try to decrypt with wrong key
        with pytest.raises(Exception):
            CryptographyEngine.decrypt_file(ciphertext, key2, iv, tag)
    
    def test_decrypt_with_corrupted_tag(self):
        """Test that decryption fails with corrupted authentication tag"""
        original_data = b"Important data"
        key = CryptographyEngine.generate_random_bytes(CryptographyEngine.KEY_SIZE)
        
        ciphertext, iv, tag = CryptographyEngine.encrypt_file(original_data, key)
        
        # Corrupt tag
        corrupted_tag = bytes([tag[0] ^ 0xFF]) + tag[1:]
        
        # Decryption should fail
        with pytest.raises(Exception):
            CryptographyEngine.decrypt_file(ciphertext, key, iv, corrupted_tag)
    
    def test_compute_hash_sha512(self):
        """Test SHA-512 hash computation"""
        data = b"Test data for hashing"
        
        hash1 = CryptographyEngine.compute_hash_sha512(data)
        hash2 = CryptographyEngine.compute_hash_sha512(data)
        
        # Same data should produce same hash
        assert hash1 == hash2
        # Hash should be hexadecimal string
        assert isinstance(hash1, str)
        assert len(hash1) == 128  # SHA-512 produces 128 hex characters
    
    def test_verify_hash(self):
        """Test hash verification"""
        data = b"Data to verify"
        
        correct_hash = CryptographyEngine.compute_hash_sha512(data)
        wrong_hash = CryptographyEngine.compute_hash_sha512(b"Different data")
        
        assert CryptographyEngine.verify_hash(data, correct_hash) is True
        assert CryptographyEngine.verify_hash(data, wrong_hash) is False
    
    def test_invalid_key_size(self):
        """Test encryption with invalid key size"""
        data = b"Test"
        wrong_key = b"short"
        
        with pytest.raises(ValueError):
            CryptographyEngine.encrypt_file(data, wrong_key)
    
    def test_invalid_iv_size(self):
        """Test decryption with invalid IV size"""
        key = CryptographyEngine.generate_random_bytes(CryptographyEngine.KEY_SIZE)
        wrong_iv = b"short"
        tag = b"x" * CryptographyEngine.TAG_SIZE
        ciphertext = b"data"
        
        with pytest.raises(ValueError):
            CryptographyEngine.decrypt_file(ciphertext, key, wrong_iv, tag)


class TestPasswordValidator:
    """Test password validation"""
    
    def test_valid_strong_password(self):
        """Test validation of strong password"""
        password = "SecurePass123!@#"
        result = PasswordValidator.validate(password)
        
        assert result["valid"] is True
        assert result["score"] >= 75
        assert len(result["feedback"]) == 0
    
    def test_weak_password_short(self):
        """Test validation of short password"""
        password = "short"
        result = PasswordValidator.validate(password)
        
        assert result["valid"] is False
        assert result["score"] < 50
        assert len(result["feedback"]) > 0
    
    def test_weak_password_no_uppercase(self):
        """Test validation of password without uppercase"""
        password = "nouppercase123!"
        result = PasswordValidator.validate(password)
        
        assert result["valid"] is False
        assert "Add uppercase" in result["feedback"]
    
    def test_weak_password_no_lowercase(self):
        """Test validation of password without lowercase"""
        password = "NOLOWERCASE123!"
        result = PasswordValidator.validate(password)
        
        assert result["valid"] is False
        assert "Add lowercase" in result["feedback"]
    
    def test_weak_password_no_numbers(self):
        """Test validation of password without numbers"""
        password = "NoNumbers!@#$"
        result = PasswordValidator.validate(password)
        
        assert result["valid"] is False
        assert "Add numbers" in result["feedback"]
    
    def test_weak_password_no_special(self):
        """Test validation of password without special characters"""
        password = "NoSpecial123"
        result = PasswordValidator.validate(password)
        
        assert result["valid"] is False
        assert "Add special characters" in result["feedback"]
    
    def test_password_score_improvement(self):
        """Test that longer passwords get higher scores"""
        short_password = "Pass1!"
        long_password = "VeryLongSecurePassword1234!@#$"
        
        short_score = PasswordValidator.validate(short_password)["score"]
        long_score = PasswordValidator.validate(long_password)["score"]
        
        assert long_score > short_score
    
    def test_password_score_range(self):
        """Test that scores are in valid range"""
        test_passwords = [
            "a",
            "short",
            "Password1",
            "SecurePassword123!@#"
        ]
        
        for pwd in test_passwords:
            result = PasswordValidator.validate(pwd)
            assert 0 <= result["score"] <= 100


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
