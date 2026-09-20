# Installation Guide

## Windows Installation

### Prerequisites
- Windows 10 (Build 1909) or later
- 1GB RAM minimum
- 500MB free disk space
- Internet connection for initial setup

### Method 1: Using Executable (Recommended for most users)

1. **Download**
   - Visit: https://github.com/yourusername/GordonSecureVault/releases
   - Download latest: `gordon-secure-vault.exe`

2. **Install**
   - Double-click `gordon-secure-vault.exe`
   - Accept User Account Control prompt
   - Application extracts and launches

3. **First Run**
   - Application creates `~/.gordon_secure_vault` directory
   - Configuration file created automatically
   - Ready to create first vault

### Method 2: From Source Code (For developers)

1. **Install Python**
   - Download Python 3.13+ from python.org
   - Run installer with "Add Python to PATH" checked
   - Verify installation:
     ```bash
     python --version
     ```

2. **Clone Repository**
   ```bash
   git clone https://github.com/yourusername/GordonSecureVault.git
   cd GordonSecureVault
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Application**
   ```bash
   python desktop/main.py
   ```

### Method 3: Build from Source

1. **Follow Method 2 steps 1-3**

2. **Build Executable**
   ```bash
   build_exe.bat
   ```
   - Creates `dist/gordon-secure-vault.exe`
   - Located in `dist/` directory

3. **Run Executable**
   - Execute `dist/gordon-secure-vault.exe`
   - No Python installation required for end users

## Android Installation

### Prerequisites
- Android 8.0 or later
- 200MB free storage space
- Internet connection

### Installation Steps

1. **Via Google Play Store**
   - Open Play Store
   - Search: "Gordon Secure Vault"
   - Tap "Install"
   - Grant requested permissions

2. **Via APK (Manual)**
   - Download: `gordon-secure-vault.apk`
   - Enable "Unknown Sources" in Settings → Security
   - Tap APK file to install
   - Grant permissions when prompted

## Verification

### Windows

1. **Check Installation**
   ```bash
   # Should show version
   gordon-secure-vault.exe --version
   ```

2. **Verify Directories**
   ```bash
   # Should exist
   %USERPROFILE%\.gordon_secure_vault\
   ```

3. **Test First Run**
   - Launch application
   - Should display Dashboard
   - No errors in console

### Troubleshooting

#### Application Won't Start
- **Solution**: Update Windows to latest version
- **Solution**: Reinstall Visual C++ Runtime
- **Solution**: Clear temp files: `%TEMP%`

#### Missing Dependencies Error
- **Solution**: Reinstall from source method
  ```bash
  pip install --upgrade -r requirements.txt
  ```

#### Port Already in Use (Development)
- **Solution**: Change port in `config.json`
- **Solution**: Stop other applications using port

#### Permission Denied
- **Solution**: Run as Administrator
- **Solution**: Check file permissions in folder properties

## Upgrading

### From Executable
1. Download latest version
2. Run new executable
3. Settings/vaults automatically migrated

### From Source
```bash
git pull origin main
pip install --upgrade -r requirements.txt
```

## Uninstallation

### Windows
1. Control Panel → Programs → Programs and Features
2. Find "Gordon Secure Vault"
3. Click "Uninstall"
4. Follow wizard

### Manual Uninstallation
1. Delete application directory
2. Delete user data (optional):
   ```bash
   rm -r %USERPROFILE%\.gordon_secure_vault
   ```

### Remove Python Dependency (if installed for this app only)
```bash
pip uninstall -r requirements.txt
```

## Post-Installation Configuration

### 1. Initial Setup
- Launch application
- Review security settings
- Customize theme (optional)
- Set auto-lock timeout

### 2. First Vault Creation
- Click "Vault Manager"
- Click "➕ New Vault"
- Enter vault name
- Set strong password
- Click "Create"

### 3. Configure Backups
- Go to "Backup Center"
- Set backup location
- Enable automatic backups (optional)
- Create first backup

### 4. Security Configuration
- Go to "Security Center"
- Review password strength
- Configure auto-lock timeout
- Enable logging if needed

## System Requirements Details

### Minimum Specifications
- **OS**: Windows 10 (Build 1909+) / Android 8.0+
- **Processor**: 1 GHz dual-core
- **RAM**: 1GB
- **Storage**: 500MB free space
- **Display**: 720p minimum

### Recommended Specifications
- **OS**: Windows 11 / Android 12+
- **Processor**: 2+ GHz quad-core
- **RAM**: 4GB+
- **Storage**: SSD with 1GB+ free space
- **Display**: 1080p or higher
- **Network**: 10+ Mbps for cloud features

## Performance Optimization

### Windows
1. Disable unnecessary startup programs
2. Enable SSD TRIM if available
3. Allocate sufficient virtual memory
4. Keep system drivers updated

### Android
1. Clear app cache regularly
2. Uninstall unused apps
3. Enable auto-backup to cloud
4. Update Android OS when available

## Network Configuration

### Firewall Rules
- No inbound connections required
- Outbound: Optional for cloud features
- Localhost only for local operations

### Proxy Support
- Configure in system settings
- Application uses system proxy automatically
- Override in `config.json` if needed

## Disk Space Requirements

### Installation
- Base application: 150-200MB
- Python runtime (from source): 100-150MB
- Dependencies: 50-100MB
- **Total**: ~300-450MB

### Runtime
- Per vault: Encrypted file size
- Backups: Same as vault size
- Logs: 10-50MB (with rotation)
- Temporary: <100MB (auto-cleanup)

## Migration from Other Applications

### From VeraCrypt
1. Create new vault in Gordon
2. Decrypt VeraCrypt volume
3. Copy files to Gordon vault
4. Delete VeraCrypt volume

### From KeePass
1. Export passwords as CSV
2. Import into Gordon (via future plugin)
3. Store CSV temporarily in vault
4. Secure delete original

## Support & Documentation

### Documentation
- `README.md` - Quick start guide
- `SECURITY.md` - Security information
- `docs/` - Detailed documentation

### Help Resources
- GitHub Issues: Report bugs
- Discussions: Ask questions
- Wiki: Community guides

### Getting Help
```bash
# View version
gordon-secure-vault --version

# View help
gordon-secure-vault --help

# View logs
cat ~/.gordon_secure_vault/logs/application.log
```

---

**Installation Version**: 1.0.0  
**Last Updated**: September 19, 2026  
**Status**: Production Ready ✓
