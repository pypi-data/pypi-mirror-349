# Quick Start Guide

Get up and running with LDA in under 5 minutes.

## Installation

LDA is available on PyPI and supports Python 3.8+. We recommend using [UV](https://github.com/astral-sh/uv) for installation:

```bash
# Using UV (recommended)
uv pip install ldanalysis

# Alternative: using pip
pip install ldanalysis
```

## Initialize Your First Project

Create a new LDA project with a simple command:

```bash
lda init
```

The interactive prompt will guide you through:
- **Project name**: Your research project title
- **Description**: Brief project overview
- **Analyst**: Your name (auto-detected from git config)
- **Directory**: Where to create the project

### Example Session

```bash
$ lda init
Welcome to LDA Project Setup! 🌟

📋 Project Details:
Project name: Clinical Trial Analysis
Description: Phase 3 trial data analysis
Analyst [Dr. Jane Smith]: 
Project directory [clinical-trial-analysis]: 

✨ Creating project structure...
✅ Project initialized successfully!
```

## Key Commands

### `lda status`
View the current state of your project:

```bash
$ lda status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 LDA Project Status
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 Project: Clinical Trial Analysis
📂 Location: /Users/jane/research/clinical-trial-analysis
🔬 Type: research
📅 Created: 2024-01-15

Project Structure:
clinical-trial-analysis/
├── lda_config.yaml      # Project configuration
├── sections/            # Analysis sections
├── data/               # Input data
├── outputs/            # Results
└── logs/               # Execution logs
```

### `lda check`
Validate your project configuration:

```bash
$ lda check
✅ Configuration valid
✅ All required fields present
✅ Project structure intact
```

### `lda sync`
Synchronize project structure with configuration:

```bash
$ lda sync
🔄 Synchronizing project structure...
✅ Created 3 new directories
✅ Updated README files
✅ Sync complete!
```

## Project Templates

Speed up setup with pre-configured templates:

```bash
# Research project template
lda init -t research

# Data science project
lda init -t minimal

# Documentation project
lda init -t documentation
```

## Configuration Management

LDA uses YAML configuration files for flexibility:

```yaml
# lda_config.yaml
project:
  name: Clinical Trial Analysis
  code: CTA2024
  description: Phase 3 trial data analysis

metadata:
  analyst: Dr. Jane Smith
  created: 2024-01-15
  version: 1.0.0

sections:
  - name: Data Preprocessing
    description: Clean and prepare raw data
  - name: Statistical Analysis
    description: Primary endpoint analysis
```

## Working with Sections

Organize your analysis into logical sections:

```bash
# Navigate to a section
cd sections/01_data_preprocessing/

# Run analysis
python run.py

# Check outputs
ls outputs/
```

## Best Practices

1. **Use descriptive project names**: Make them searchable and meaningful
2. **Version control everything**: Commit early and often
3. **Document as you go**: Update section READMEs
4. **Follow naming conventions**: Use the built-in naming system
5. **Regular validation**: Run `lda check` periodically

## Next Steps

Ready to dive deeper? Check out our [detailed tutorial](tutorial.md) for:
- Advanced configuration options
- Custom templates
- Integration with analysis tools
- Team collaboration features

---

Need help? Run `lda --help` or visit our [documentation](https://ldanalysis.readthedocs.io)