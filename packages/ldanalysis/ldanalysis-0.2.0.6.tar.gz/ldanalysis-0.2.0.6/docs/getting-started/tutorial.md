# Getting Started with LDA

This tutorial will walk you through installing Linked Document Analysis (LDA) and creating your first project.

## Prerequisites

- Python 3.9 or higher
- [uv](https://github.com/astral-sh/uv) package manager
- Basic familiarity with command line

## Installation

Install LDA using uv:

```bash
uv tool install ldanalysis
```

Verify the installation:

```bash
ldanalysis --version
```

## Creating Your First Project

### Basic Initialization

Create a new LDA project with a descriptive name:

```bash
ldanalysis init --name "Climate Analysis 2024"
```

This creates:
- A project folder: `climate_analysis_2024/`
- Configuration file: `climate_analysis_2024_config.yaml`
- Playground directory: `lda_playground/`
- Project manifest for tracking

### Initialization with Sections

Create a project with predefined sections:

```bash
ldanalysis init --name "Drug Study" --sections "protocol,data,analysis,figures"
```

Each section includes:
- Input/output directories
- Logs directory
- Run script (`run.py` by default)
- README file

### Multi-Language Support

Generate both Python and R scripts:

```bash
ldanalysis init --name "Stats Project" --sections "modeling" --language both
```

Options:
- `python`: Python scripts only (default)
- `r`: R scripts only  
- `both`: Both Python and R scripts

### Minimal Projects

Create a project without sections or playground:

```bash
ldanalysis init --name "Quick Test" --no-playground
```

This creates just the basic structure without predefined sections.

## Working with Projects

### Check Project Status

View project information and status:

```bash
ldanalysis status
```

Shows:
- Project metadata
- Section list
- File counts
- Last activity

### Adding Sections Later

You can add sections after initialization using the sync command:

1. Edit your project's config file (e.g., `climate_analysis_2024_config.yaml`):

```yaml
sections:
- name: introduction
  inputs: []
  outputs: []
- name: methodology  # New section
  inputs: []
  outputs: []
```

2. Sync the project structure:

```bash
ldanalysis sync
```

This creates the new section with all standard directories and scripts.

### Sync with Dry Run

Preview changes before applying them:

```bash
ldanalysis sync --dry-run
```

## Project Structure

A typical LDA project looks like:

```
climate_analysis_2024/
├── climate_analysis_2024_config.yaml
├── climate_analysis_2024/
│   ├── lda_manifest.csv
│   ├── lda_playground/
│   │   ├── experiments/
│   │   ├── scratch/
│   │   ├── notebooks/
│   │   └── example_exploration.py
│   ├── climate_analysis_2024_sec01_introduction/
│   │   ├── README.md
│   │   ├── inputs/
│   │   ├── outputs/
│   │   ├── logs/
│   │   ├── run.py
│   │   └── run.R (if language=both)
│   └── climate_analysis_2024_sec02_methodology/
│       └── ... (same structure)
```

## Configuration Files

Configuration files are named after your project:
- Project: "Climate Analysis 2024"
- Config: `climate_analysis_2024_config.yaml`

Key configuration options:

```yaml
project:
  name: Climate Analysis 2024
  code: climate_analysis_2024
  analyst: Your Name
  create_playground: true
  language: python

sections:
- name: data_prep
  inputs: []
  outputs: []
- name: analysis
  inputs: []
  outputs: []
```

## The Playground

The `lda_playground` directory is for exploratory work:

- `experiments/`: Try out analysis approaches
- `scratch/`: Temporary work
- `notebooks/`: Jupyter notebooks
- Example scripts in your chosen language(s)

Use it to test ideas before formalizing them into sections.

## Working with Sections

Each section represents a distinct analysis phase:

1. Navigate to a section:
   ```bash
   cd climate_analysis_2024/climate_analysis_2024_sec01_data_prep
   ```

2. Add input files to `inputs/`

3. Edit the run script (`run.py` or `run.R`)

4. Execute the analysis:
   ```bash
   python run.py
   # or
   Rscript run.R
   ```

5. Results are saved to `outputs/`

## Tracking Files

Register files in the manifest:

```bash
ldanalysis track data.csv --section data_prep --type input
ldanalysis track results.png --section analysis --type output
```

View tracked changes:

```bash
ldanalysis changes
```

## Best Practices

1. **Use descriptive project names**: They become folder and config names
2. **Plan sections upfront**: Map to document sections
3. **Start in playground**: Test approaches before formalizing
4. **Track important files**: Maintain provenance
5. **Use sync for updates**: Add sections as needed
6. **Document your work**: Update READMEs in each section

## Next Steps

- Explore the [User Guide](../user-guide/concepts.md) for detailed concepts
- Read about [Configuration](../user-guide/configuration.md) options
- Learn about [File Tracking](../user-guide/tracking.md)
- Understand [Project Syncing](../user-guide/syncing-projects.md)

## Quick Reference

```bash
# Install
uv tool install ldanalysis

# Create project
ldanalysis init --name "My Project"

# With sections
ldanalysis init --name "My Project" --sections "intro,methods,results"

# With R support
ldanalysis init --name "My Project" --language r

# Both languages
ldanalysis init --name "My Project" --language both

# No playground
ldanalysis init --name "My Project" --no-playground

# Check status
ldanalysis status

# Sync structure
ldanalysis sync

# Dry run
ldanalysis sync --dry-run

# Track files
ldanalysis track file.csv --section intro --type input

# View changes
ldanalysis changes
```