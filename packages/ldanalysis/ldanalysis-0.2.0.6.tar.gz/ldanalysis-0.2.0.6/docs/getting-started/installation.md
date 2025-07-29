# Installation

Getting started with LDA is simple. The recommended way is using the `uv` package manager.

## Requirements

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) package manager (recommended)
- Git (optional, for development installation)

## Quick Install with uv (Recommended)

The fastest way to install LDA is using uv:

```bash
uv tool install ldanalysis
```

That's it! You can now start using LDA. Verify your installation:

```bash
ldanalysis --version
```

## Alternative Installation Methods

### Using pip

If you prefer traditional pip installation:

```bash
pip install ldanalysis
```

Note: The package name is `ldanalysis` (not `lda` which is used by another package).

### Using pipx (Isolated Environment)

For an isolated installation:

```bash
pipx install ldanalysis
```

### From Source

To install the latest development version:

```bash
git clone https://github.com/drpedapati/LDA.git
cd LDA
uv pip install -e .
```

## Platform-Specific Instructions

### macOS

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install LDA
uv tool install ldanalysis
```

### Windows

```powershell
# Install uv using PowerShell
irm https://astral.sh/uv/install.ps1 | iex

# Install LDA
uv tool install ldanalysis
```

### Linux

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install LDA
uv tool install ldanalysis
```

## Verify Installation

After installation, verify that LDA is working correctly:

```bash
# Check version
ldanalysis --version

# View help
ldanalysis --help

# Test initialization
ldanalysis init --name "Test Project" --dry-run
```

## Upgrading

To upgrade to the latest version:

```bash
uv tool upgrade ldanalysis
```

## Development Installation

For contributors and developers:

```bash
# Clone the repository
git clone https://github.com/drpedapati/LDA.git
cd LDA

# Create virtual environment
uv venv

# Install in development mode
uv pip install -e .

# Install development dependencies
uv pip install -e ".[dev]"
```

## Troubleshooting

### Common Issues

**Command Not Found**

If `ldanalysis` is not found after installation:

```bash
# Check if uv tools are in PATH
export PATH="$HOME/.local/bin:$PATH"

# Or reinstall
uv tool install --force ldanalysis
```

**Permission Denied**

On Unix systems, you may need to add the tools directory to PATH:

```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc
```

**Package Name Confusion**

Remember:
- Install with: `uv tool install ldanalysis`
- Run with: `ldanalysis` (not `lda`)

### Getting Help

If you encounter issues:

1. Check the [troubleshooting guide](../troubleshooting.md)
2. Search [existing issues](https://github.com/drpedapati/LDA/issues)
3. Ask in [discussions](https://github.com/drpedapati/LDA/discussions)
4. Report a [new issue](https://github.com/drpedapati/LDA/issues/new)

## Next Steps

Now that you have LDA installed, proceed to:

- [Quick Start](quickstart.md) - Learn the basics in 5 minutes
- [Tutorial](tutorial.md) - Comprehensive walkthrough
- [First Project](first-project.md) - Build your first LDA project