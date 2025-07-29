# Command Line Interface

LDA provides a comprehensive command-line interface through the `ldanalysis` command.

## Installation and Usage

After installing with uv:

```bash
uv tool install ldanalysis
```

You can run commands using:

```bash
ldanalysis <command> [options]
```

Note: While the package provides both `lda` and `ldanalysis` commands, we recommend using `ldanalysis` to avoid conflicts with other packages.

## Available Commands

### Project Management
- `init` - Initialize a new LDA project
- `status` - Show project status and information
- `sync` - Sync project structure with configuration

### File Tracking
- `track` - Register files in the manifest
- `changes` - Show file changes and modifications
- `history` - Display project history

### Data Management
- `validate` - Validate project structure and files
- `export` - Export manifest or reports

### Documentation
- `docs serve` - Serve documentation locally
- `docs build` - Build documentation site

## Global Options

Options available for all commands:

- `--help, -h` - Show help message
- `--version` - Show version information
- `--verbose, -v` - Enable verbose output
- `--quiet, -q` - Suppress non-error output
- `--config, -c` - Specify configuration file

## Common Workflows

### Creating a New Project

```bash
# Basic project
ldanalysis init --name "My Project"

# With sections
ldanalysis init --name "Study 2024" --sections "data,analysis,results"

# Multi-language support
ldanalysis init --name "Stats Project" --language both

# Without playground
ldanalysis init --name "Minimal" --no-playground
```

### Syncing Projects

```bash
# Preview changes
ldanalysis sync --dry-run

# Apply changes
ldanalysis sync

# Use specific config
ldanalysis sync --config project_config.yaml
```

### Tracking Files

```bash
# Track input file
ldanalysis track data.csv --section analysis --type input

# Track output file
ldanalysis track results.png --section results --type output

# View tracked changes
ldanalysis changes
```

## Exit Codes

- `0` - Success
- `1` - General error
- `2` - Command line usage error
- `130` - Operation cancelled by user

## Environment Variables

LDA respects these environment variables:

- `LDA_CONFIG` - Default configuration file path
- `NO_COLOR` - Disable colored output
- `LDA_VERBOSE` - Enable verbose output by default

## Shell Completion

Enable shell completion for your shell:

```bash
# Bash
eval "$(_LDANALYSIS_COMPLETE=bash_source ldanalysis)"

# Zsh
eval "$(_LDANALYSIS_COMPLETE=zsh_source ldanalysis)"

# Fish
_LDANALYSIS_COMPLETE=fish_source ldanalysis | source
```

## Getting Help

For detailed help on any command:

```bash
ldanalysis <command> --help
```

For general help:

```bash
ldanalysis --help
```