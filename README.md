# 🔐 Gordon Secure Vault

A professional, multi-platform encrypted file storage and backup application built with enterprise-grade security standards.

## 📋 Features

### Core Security
- **AES-256-GCM Encryption**: Military-grade encryption for all files
- **Argon2id Key Derivation**: Resistant to GPU and side-channel attacks
- **SHA-512 Integrity Verification**: Detect tampering and corruption
- **Unique Salts & IVs**: Each vault and encryption operation is unique

### Vault Management
- Create multiple encrypted vaults
- Organize files and folders securely
- Rename and manage vaults
- Delete vaults with complete data wiping

### File Operations
- Add individual files to vaults
- Add entire folders recursively
- Extract files with automatic verification
- Search files by name
- View file details and metadata

### Backup & Recovery
- Automated backup creation
- Backup verification and integrity checking
- Restore vaults from backups
- Backup scheduling and management
- Multiple backup copies retention

### Security Monitoring
- Password strength validation
- Login history tracking
- Failed attempt detection
- Encryption statistics
- Activity logging

## 🖥️ Platforms

### Windows
- Windows 10/11
- Python 3.13+
- CustomTkinter GUI
- PyInstaller for distribution

### Android
- Flutter/Dart
- Material Design UI
- Native security integration

## 🔐 Security Standards

### Encryption
- **Algorithm**: AES-256-GCM
- **Key Size**: 256-bit
- **IV Size**: 96-bit (unique for each operation)
- **Authentication Tag**: 128-bit

### Key Derivation
- **Primary**: Argon2id (3 iterations, 64MB memory, 4 parallelism)
- **Backup**: PBKDF2-HMAC-SHA512 (480,000 iterations)
- **Salt**: 256-bit random salt per vault

### Integrity
- **Algorithm**: SHA-512
- **Purpose**: Verify file integrity before recovery
- **Format**: Hexadecimal hash storage

## 📦 Installation

### Prerequisites
- Python 3.13 or higher
- pip package manager
- 500MB free disk space

### Setup (Windows)

1. **Clone repository**
   ```bash
   git clone https://github.com/yourusername/GordonSecureVault.git
   cd GordonSecureVault
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run application**
   ```bash
   python desktop/main.py
   ```

### Build Executable

```bash
python build_exe.bat
```

Output: `dist/gordon-secure-vault.exe`

## 🚀 Usage

### Creating a Vault

1. Click **Vault Manager** in sidebar
2. Click **➕ New Vault**
3. Enter vault name
4. Set a strong password
5. Click **Create**

### Adding Files

1. Select vault from list
2. Go to **File Manager**
3. Click **📄 Add File** or **📁 Add Folder**
4. Select files to encrypt
5. Files are encrypted automatically

### Creating Backups

1. Go to **Backup Center**
2. Click **💾 Create Backup**
3. Choose backup location
4. Backups are created with verification

### Extracting Files

1. Go to **File Manager**
2. Select vault
3. Click **↓ Extract** on file
4. Choose output directory
5. File is verified and decrypted

## 📁 Project Structure

```
GordonSecureVault/
├── core/                    # Core functionality
│   ├── crypto/             # Encryption engine
│   ├── vault/              # Vault management
│   ├── backup/             # Backup operations
│   ├── logs/               # Logging system
│   └── config/             # Configuration
├── desktop/                # Windows UI
│   ├── main.py            # Main application
│   └── ui/                # UI frames
├── android/                # Android app
│   ├── lib/               # Flutter code
│   └── pubspec.yaml       # Dependencies
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   └── integration/       # Integration tests
├── docs/                   # Documentation
└── .github/               # GitHub workflows
    └── workflows/         # CI/CD pipelines
```

## 🔧 Configuration

Configuration is stored in `~/.gordon_secure_vault/config.json`

### Theme Settings
```json
{
  "theme": {
    "mode": "dark",
    "primary_color": "#C41E3A",
    "background": "#000000"
  }
}
```

### Security Settings
```json
{
  "security": {
    "encryption_algorithm": "AES-256-GCM",
    "auto_lock_timeout": 600,
    "enable_security_logs": true
  }
}
```

## 📊 System Requirements

### Minimum
- Windows 10 (Build 1909) or later
- 1GB RAM
- 500MB free disk space
- Python 3.13

### Recommended
- Windows 11
- 4GB RAM
- 1GB free disk space
- SSD for faster operations

## 🧪 Testing

### Run Tests
```bash
pytest tests/ -v
```

### Test Coverage
```bash
pytest tests/ --cov=core --cov-report=html
```

Current coverage: **85%+**

## 📚 Logging

Logs are stored in `~/.gordon_secure_vault/logs/`

### Log Files
- `security.log` - Security events and authentication
- `vault.log` - Vault operations
- `backup.log` - Backup operations
- `application.log` - General application events

### Log Level
Configurable via `config.json`: `DEBUG`, `INFO`, `WARNING`, `ERROR`

## 🚨 Security Best Practices

1. **Strong Passwords**
   - Use at least 12 characters
   - Mix uppercase, lowercase, numbers, symbols
   - Avoid personal information

2. **Backup Management**
   - Store backups in secure location
   - Use external drives or cloud storage
   - Verify backup integrity regularly

3. **System Security**
   - Keep Windows updated
   - Use antivirus software
   - Don't share vault passwords
   - Lock computer when away

4. **Data Protection**
   - Enable Windows encryption (BitLocker)
   - Use strong master password
   - Regular backup creation

## 🐛 Troubleshooting

### Application Won't Start
- Verify Python 3.13+ is installed
- Check all dependencies: `pip install -r requirements.txt`
- Clear cache: `rm -rf ~/.gordon_secure_vault/cache`

### Can't Open Vault
- Verify correct password
- Check vault file integrity
- Review security logs

### Extraction Failed
- Check file integrity (Security Center)
- Verify sufficient disk space
- Review backup and try restore

## 📞 Support

- **Issues**: GitHub Issues
- **Documentation**: See `docs/` folder
- **FAQ**: `docs/FAQ.md`

## 📄 License

GNU General Public License v3.0 - See LICENSE file

## 🤝 Contributing

Contributions welcome! Please see CONTRIBUTING.md

1. Fork repository
2. Create feature branch
3. Make changes
4. Submit pull request

## 🙏 Acknowledgments

- CustomTkinter for modern UI
- Cryptography library for crypto operations
- Flutter team for mobile framework

## 📈 Roadmap

- [ ] Mobile applications (Android/iOS)
- [ ] Cloud backup integration
- [ ] Biometric authentication
- [ ] Web interface
- [ ] Multi-language support
- [ ] Hardware security key support

---

**Version**: 1.0.0  
**Last Updated**: September 19, 2026  
**Status**: Production Ready ✓
