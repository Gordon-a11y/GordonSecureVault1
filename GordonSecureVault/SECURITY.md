# Security Policy

## 🔐 Security Standards

Gordon Secure Vault uses industry-standard cryptographic algorithms to protect user data:

### Encryption
- **Algorithm**: AES-256-GCM (Advanced Encryption Standard with Galois/Counter Mode)
- **Key Size**: 256-bit
- **Nonce Size**: 96-bit (unique for each encryption operation)
- **Authentication Tag**: 128-bit for integrity verification
- **Mode**: Authenticated encryption with associated data (AEAD)

### Key Derivation
- **Primary Method**: Argon2id (memory-hard, resistant to GPU attacks)
  - Time Cost: 3 iterations
  - Memory Cost: 64MB per operation
  - Parallelism: 4 threads
  - Output: 256-bit key

- **Secondary Method**: PBKDF2-HMAC-SHA512 (NIST approved)
  - Iterations: 480,000
  - Hash Algorithm: SHA-512
  - Salt: 256-bit random salt per vault

### Integrity & Authentication
- **Algorithm**: SHA-512 (Secure Hash Algorithm)
- **Output Size**: 512-bit (64 bytes)
- **Format**: Hexadecimal encoding
- **Usage**: Verify file integrity before decryption

### Random Number Generation
- **Source**: `os.urandom()` - Cryptographically secure OS-level randomness
- **Salt Size**: 256-bit for each vault
- **IV Size**: 96-bit for each encryption operation
- **Source Quality**: System entropy pool (dev/urandom on Unix, CryptGenRandom on Windows)

## 🛡️ Security Features

### Vault Protection
- No plaintext passwords stored
- No plaintext encryption keys stored
- Each vault has unique salt and parameters
- Password verification via secure comparison

### File Protection
- Each file encrypted individually
- Unique IV for every encryption
- Authentication tag prevents tampering
- Integrity verification before decryption
- File metadata protected (size, name encrypted)

### System Security
- Secure memory handling
- Sensitive data cleared from memory after use
- No temporary unencrypted copies
- Secure key derivation with high entropy
- Auto-lock functionality (configurable timeout)

### Logging Security
- Security events logged separately
- Log rotation to prevent overflow
- Log files stored securely
- Sensitive information not logged

## 🚨 Security Considerations

### What Gordon Secure Vault Protects Against
- Unauthorized file access
- Data interception
- File tampering or corruption
- Brute-force password attacks (via Argon2id)
- Side-channel attacks (memory-hard algorithms)

### What Gordon Secure Vault Does NOT Protect Against
- Physical device theft (use OS-level encryption like BitLocker)
- Malware on your system (use antivirus software)
- Weak or leaked master passwords
- Shoulder surfing or keyloggers
- Social engineering attacks
- Zero-day vulnerabilities in cryptographic libraries

## 🔑 Password Security

### Best Practices for Strong Passwords
1. **Length**: Use at least 12 characters (20+ recommended)
2. **Complexity**: Mix uppercase, lowercase, numbers, special characters
3. **Uniqueness**: Don't reuse passwords from other services
4. **Unpredictability**: Avoid personal information, dictionary words
5. **Rotation**: Consider changing passwords periodically

### Password Strength Checker
Application includes password validator:
- Minimum 8 characters for acceptance
- Bonus points for 12+ characters
- Requires uppercase letters (15 points)
- Requires lowercase letters (15 points)
- Requires numbers (15 points)
- Requires special characters (25 points)
- Score 50+ considered acceptable

## 🔍 Verification & Testing

### Security Testing
- Unit tests for cryptographic operations
- Integration tests for vault operations
- Key derivation verification
- Encryption/decryption round-trip tests
- Integrity check validation

### Code Quality
- Static analysis with flake8 and pylint
- Type checking with mypy
- Security scanning with Bandit
- Dependency vulnerability checks with Safety
- Code coverage target: 80%+

### Continuous Integration
- Automated testing on every commit
- Security scans on every pull request
- Build verification before release
- Coverage reporting and tracking

## 🔔 Reporting Security Issues

### Responsible Disclosure
If you discover a security vulnerability:

1. **DO NOT** open a public GitHub issue
2. **DO** email security details to: security@gordonvault.dev
3. Include:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Your name/contact info (optional)

### What to Expect
- Acknowledgment within 48 hours
- Investigation and assessment
- Fix development (if required)
- Responsible disclosure timeline
- Credit in security advisory

### Response Timeline
- Critical: Fix within 7 days
- High: Fix within 14 days
- Medium: Fix within 30 days
- Low: Fix in next release

## 📋 Security Audit Checklist

Before using Gordon Secure Vault:

- [ ] Download from official repository
- [ ] Verify code on GitHub
- [ ] Review security.md (this file)
- [ ] Enable BitLocker/device encryption
- [ ] Install antivirus software
- [ ] Keep Windows updated
- [ ] Use strong master password
- [ ] Regular backup creation
- [ ] Test backup restoration

## 🔄 Dependency Management

### Third-Party Libraries
All dependencies are carefully vetted:

```
cryptography >= 41.0.0    # Industry-standard crypto library
argon2-cffi >= 23.0.0     # Argon2 key derivation
customtkinter >= 5.2.0    # Modern GUI framework
```

### Dependency Monitoring
- Regular security updates
- Vulnerability scanning (Safety)
- Automated dependency updates (Dependabot)
- Version pinning in requirements.txt

## 🔐 Cryptographic Assumptions

Security of this application assumes:
- Correct implementation of cryptographic libraries
- Proper use of cryptographic primitives
- No flaws in Python/OS randomness
- No active cryptanalysis attacks
- No quantum computers (relevant in future)

## 📚 Additional Resources

### Learning More
- [OWASP Cryptographic Storage Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Cryptographic_Storage_Cheat_Sheet.html)
- [NIST Cryptographic Standards](https://csrc.nist.gov/projects/cryptographic-standards-and-guidelines/)
- [AES-GCM Documentation](https://nvlpubs.nist.gov/nistpubs/Legacy/SP/nistspecialpublication800-38d.pdf)
- [Argon2 Paper](https://github.com/P-H-C/phc-winner-argon2/blob/master/argon2-specs.pdf)

### Security Tools
- [KeePass](https://keepass.info/) - Reference password manager
- [VeraCrypt](https://www.veracrypt.fr/) - Full disk encryption
- [Veracrypt](https://www.veracrypt.fr/) - USB encryption

## 📞 Contact

- **Security Issues**: security@gordonvault.dev
- **General Support**: support@gordonvault.dev
- **GitHub Issues**: https://github.com/yourusername/GordonSecureVault/issues

---

**Last Updated**: September 19, 2026  
**Version**: 1.0.0  
**Status**: Production Ready
