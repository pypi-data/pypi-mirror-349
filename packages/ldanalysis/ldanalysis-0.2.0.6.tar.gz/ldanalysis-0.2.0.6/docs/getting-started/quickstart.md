# Quick Start

Get up and running with LDA in 5 minutes. This guide will walk you through creating your first project.

## Installation

Install LDA using uv:

```bash
uv tool install ldanalysis
```

## Initialize Your First Project

Create a new LDA project (analyst is required):

```bash
ldanalysis init --name "My Research Project" --analyst "your.name"
```

Or set up a profile first (recommended):

```bash
# One-time setup
ldanalysis profile setup

# Then create projects with fewer parameters
ldanalysis init --name "My Research Project"
```

This creates:
- Project folder: `my_research_project/`
- Config file: `my_research_project_config.yaml`
- Playground directory for experimentation
- Project manifest for tracking

## Create a Project with Sections

Initialize with predefined sections:

```bash
ldanalysis init --name "Climate Study 2024" --analyst "jane.doe" --sections "data,analysis,results"
```

Each section includes:
- Input/output directories
- Logs directory
- Run script (Python by default)
- README file

## Multi-Language Support

Create a project with both Python and R scripts:

```bash
ldanalysis init --name "Stats Analysis" --analyst "your.name" --sections "modeling" --language both
```

## Check Project Status

View current project state:

```bash
ldanalysis status
```

Output:
```
Project: Climate Study 2024
Code: climate_study_2024
Sections: 3
Total files: 0
Last activity: Never
```

## Add Sections Later

Update your config file and sync:

1. Edit `climate_study_2024_config.yaml`:
```yaml
sections:
- name: data
  inputs: []
  outputs: []
- name: analysis
  inputs: []
  outputs: []
- name: results
  inputs: []
  outputs: []
- name: discussion  # New section
  inputs: []
  outputs: []
```

2. Sync the structure:
```bash
ldanalysis sync
```

## Project Structure Overview

```
climate_study_2024/
├── climate_study_2024_config.yaml
└── climate_study_2024/
    ├── lda_manifest.csv
    ├── lda_playground/
    │   ├── experiments/
    │   ├── scratch/
    │   └── notebooks/
    ├── climate_study_2024_sec01_data/
    │   ├── inputs/
    │   ├── outputs/
    │   ├── logs/
    │   └── run.py
    └── climate_study_2024_sec02_analysis/
        └── ... (same structure)
```

## Quick Command Reference

```bash
# Install LDA
uv tool install ldanalysis

# Set up profile (one-time)
ldanalysis profile setup

# Create basic project
ldanalysis init --name "Project Name" --analyst "your.name"

# Create with sections
ldanalysis init --name "Project" --analyst "your.name" --sections "intro,methods,results"

# Multi-language support
ldanalysis init --name "Project" --analyst "your.name" --language both

# Check status
ldanalysis status

# Sync with config
ldanalysis sync

# Preview sync changes
ldanalysis sync --dry-run

# Track files
ldanalysis track file.csv --section data --type input

# View changes
ldanalysis changes
```

## Interactive Example

Try this complete workflow:

```bash
# 1. Create a demo project
ldanalysis init --name "Drug Study Demo" \
  --analyst "demo.user" \
  --sections "protocol,data,analysis" \
  --language both

# 2. Navigate to project
cd drug_study_demo/drug_study_demo

# 3. Check status
ldanalysis status

# 4. Add a new section via config
echo '- name: figures
  inputs: []
  outputs: []' >> ../drug_study_demo_config.yaml

# 5. Sync the changes
ldanalysis sync

# 6. List the new structure
ls -la
```

## Key Concepts

- **Projects**: Named workspaces (e.g., "Climate Analysis 2024")
- **Sections**: Distinct analysis phases mapping to document sections
- **Playground**: Experimental area for testing ideas
- **Config Files**: YAML files named after your project
- **Manifest**: Tracks all files and changes

## Tips for Success

1. **Use descriptive names**: Your project name becomes the folder and config name
2. **Plan sections**: Think about your document structure upfront
3. **Use playground**: Test ideas before formalizing into sections
4. **Sync regularly**: Keep your structure aligned with the config
5. **Track important files**: Maintain provenance for key inputs/outputs

## Next Steps

- Read the full [Tutorial](tutorial.md) for detailed guidance
- Explore [Configuration Options](../user-guide/configuration.md)
- Learn about [Project Syncing](../user-guide/syncing-projects.md)
- Understand [File Tracking](../user-guide/tracking.md)