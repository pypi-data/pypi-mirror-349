# Installation Guide

This guide covers all methods to install LDAnalysis (LDA) on your system.

## Quick Install

For most users, we recommend using UV:

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install LDAnalysis
uv tool install ldanalysis
```

## Detailed Installation Methods

### Method 1: UV Tool Installation (Recommended)

[UV](https://github.com/astral-sh/uv) is a fast, reliable Python package installer that's perfect for installing command-line tools like LDAnalysis.

#### Step 1: Install UV

**macOS and Linux:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Windows:**
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Alternative installation methods:**
```bash
# Using pip
pip install uv

# Using pipx
pipx install uv

# Using Homebrew (macOS)
brew install uv

# Using Cargo
cargo install uv
```

#### Step 2: Install LDAnalysis

```bash
# Install LDAnalysis as a global tool
uv tool install ldanalysis

# The command is now available globally
lda --version
```

#### Step 3: Upgrade LDAnalysis

```bash
# Upgrade to the latest version
uv tool install --upgrade ldanalysis
```

#### Advantages of UV:
- ✅ Fast installation and dependency resolution
- ✅ Isolated environments prevent conflicts
- ✅ Easy to upgrade and manage
- ✅ No virtual environment needed
- ✅ Cross-platform support

### Method 2: Development Installation

For contributors or testing latest features with UV:

```bash
# Clone the repository (or fork it first on GitHub)
git clone https://github.com/cincineuro/ldanalysis.git
# Or clone your fork:
# git clone https://github.com/YOUR_USERNAME/ldanalysis.git

# Install in development mode with UV
uv tool install --upgrade -e /path/to/ldanalysis

# Now lda command will use your local development version
lda --version

# For development dependencies, cd into the repo
cd /path/to/ldanalysis
pip install ".[dev,docs,test]"

# Run tests
pytest

# Build documentation
mkdocs serve
```

This approach:
- Uses UV for the tool installation
- Allows real-time testing of code changes
- Maintains isolation from system Python
- Makes it easy to switch between stable and development versions

### Method 3: pipx Installation

[pipx](https://pypa.github.com/pipx/) is an alternative to UV for installing Python applications:

```bash
# Install pipx
python -m pip install --user pipx
python -m pipx ensurepath

# Install LDAnalysis
pipx install ldanalysis

# Upgrade
pipx upgrade ldanalysis
```

### Method 4: Install from GitHub with UV

Install directly from GitHub for specific versions:

```bash
# Install from main branch
uv pip install git+https://github.com/cincineuro/ldanalysis.git

# Install specific tag
uv pip install git+https://github.com/cincineuro/ldanalysis.git@v0.2.0

# Install from your fork
uv pip install git+https://github.com/YOUR_USERNAME/ldanalysis.git@your-branch
```

## Platform-Specific Instructions

### macOS

```bash
# Using Homebrew to install UV
brew install uv

# Install LDAnalysis
uv tool install ldanalysis

# Or install UV with curl
curl -LsSf https://astral.sh/uv/install.sh | sh
uv tool install ldanalysis
```

### Ubuntu/Debian

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install LDAnalysis
uv tool install ldanalysis

# Alternative: Install UV with pipx
pipx install uv
uv tool install ldanalysis
```

### Windows

```bash
# Using Windows Terminal or PowerShell

# Install UV
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Install LDAnalysis
uv tool install ldanalysis

# Alternative: Install UV with pip
pip install --user uv
uv tool install ldanalysis
```

### Conda/Mamba Environments

If you use Conda or Mamba:

```bash
# Install UV in your base environment
conda activate base
pip install uv

# Install LDAnalysis as a tool
uv tool install ldanalysis

# Or use pipx in conda
conda install -c conda-forge pipx
pipx install ldanalysis
```

## Verification

After installation, verify LDAnalysis is working:

```bash
# Check version
lda --version

# View help
lda --help

# Alternative command
ldanalysis --help

# Check installation location
which lda  # macOS/Linux
where lda  # Windows
```

## Troubleshooting

### Command Not Found

If `lda` command is not found:

1. **Check PATH**:
   ```bash
   echo $PATH
   # Ensure Python scripts directory is in PATH
   ```

2. **Find installation location**:
   ```bash
   pip show ldanalysis
   # Look for Location and Scripts fields
   ```

3. **Add to PATH manually**:
   ```bash
   # Find Python scripts directory
   python -m site --user-base
   
   # Add to PATH (add to ~/.bashrc or ~/.zshrc)
   export PATH="$PATH:$(python -m site --user-base)/bin"
   ```

4. **Try alternative command**:
   ```bash
   python -m lda --version
   ```

### Permission Errors

If you get permission errors:

1. **Use UV** (recommended):
   ```bash
   uv tool install ldanalysis
   ```

2. **Use pipx**:
   ```bash
   pipx install ldanalysis
   ```

3. **Check UV installation**:
   ```bash
   # Reinstall UV for current user
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### Python Version Issues

LDAnalysis requires Python 3.8+:

```bash
# Check Python version
python --version

# Install specific Python version
# macOS with Homebrew
brew install python@3.11

# Ubuntu
sudo apt install python3.11

# Windows
# Download from python.org
```

### Dependency Conflicts

If you encounter dependency conflicts:

1. **Use UV** (recommended):
   ```bash
   # UV automatically handles dependencies
   uv tool install ldanalysis
   ```

2. **Use pipx**:
   ```bash
   # pipx creates isolated environments
   pipx install ldanalysis
   ```

3. **Force reinstall with UV**:
   ```bash
   # Reinstall to fix conflicts
   uv tool install --upgrade --force-reinstall ldanalysis
   ```

## Uninstallation

To remove LDAnalysis:

```bash
# UV
uv tool uninstall ldanalysis

# pipx
pipx uninstall ldanalysis
```

## Next Steps

After installation:

1. [Set up your user profile](tutorial.md#first-time-setup)
2. [Create your first project](index.md#quick-start)
3. [Read the complete tutorial](tutorial.md)

## Getting Help

- **Documentation**: `lda docs`
- **Command help**: `lda --help`
- **GitHub Issues**: [Report problems](https://github.com/cincineuro/ldanalysis/issues)
- **Community**: Join our discussions on GitHub