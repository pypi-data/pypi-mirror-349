---
title: Complete LDAnalysis Tutorial
description: Comprehensive guide to using LDAnalysis for research project management
---

# Complete LDAnalysis Tutorial

This tutorial covers all features of LDAnalysis with practical examples and best practices.

## Table of Contents

1. [Installation and Setup](#installation-and-setup)
2. [Creating Your First Project](#creating-your-first-project)
3. [Project Configuration](#project-configuration)
4. [Working with Sections](#working-with-sections)
5. [File Tracking and Provenance](#file-tracking-and-provenance)
6. [Naming Conventions](#naming-conventions)
7. [Advanced Features](#advanced-features)
8. [Best Practices](#best-practices)
9. [Troubleshooting](#troubleshooting)

## Installation and Setup

### System Requirements

- Python 3.8 or higher
- uv (for recommended installation method)
- Git (optional for development)
- Text editor (VS Code, vim, etc.)

### Installation Methods

#### Method 1: Using UV Tool (Recommended for Global Use)

UV is a fast Python package installer that makes it easy to install Python tools globally.

**Step 1: Install UV**

macOS and Linux:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows:
```bash
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Step 2: Install LDAnalysis**
```bash
# Install LDAnalysis as a global tool
uv tool install ldanalysis

# Verify installation
lda --version

# Upgrade to latest version
uv tool install --upgrade ldanalysis
```

**Advantages of UV:**
- Fast installation and dependency resolution
- Isolated tool environments prevent conflicts
- Easy upgrades and uninstalls
- No need for virtual environments for tools

#### Method 2: Development Installation

For contributing or using the latest development version:

```bash
# Clone repository (or fork it first)
git clone https://github.com/cincineuro/ldanalysis.git
# Or your fork:
# git clone https://github.com/YOUR_USERNAME/ldanalysis.git

# Install in development mode with UV
uv tool install --upgrade -e /path/to/ldanalysis

# Verify it's using your development version
lda --version

# Install development dependencies
cd /path/to/ldanalysis
pip install ".[dev,docs,test]"

# Run tests to verify
pytest

# Start documentation server
mkdocs serve
```

Development installation benefits:
- Changes to code are immediately available
- Easy to test modifications
- Can switch between stable and dev versions
- Maintains clean system Python

### Post-Installation Setup

1. **Verify Installation**:
   ```bash
   # Check installation
   lda --version
   
   # View help
   lda --help
   ```

2. **Check Available Commands**:
   ```bash
   # List all commands
   lda --help
   
   # Get help for specific command
   lda init --help
   ```

3. **System Check**:
   ```bash
   # Check version and available commands
   lda --version
   lda --help
   ```

### Troubleshooting Installation

**Issue: Command not found**
```bash
# Check if lda is in PATH
which lda

# Try using full package name
ldanalysis --version

# For UV installations, refresh shell
source ~/.bashrc  # or ~/.zshrc
```

**Issue: Permission denied**
```bash
# Use UV tool (recommended)
uv tool install ldanalysis

# Or use pipx
pipx install ldanalysis
```

**Issue: Python version mismatch**
```bash
# Check Python version
python --version

# Use specific Python version
python3.9 -m pip install ldanalysis
```

### First-Time Setup

When you first run LDA, you'll be prompted to create a profile:

```bash
lda init
```

If no profile exists, you'll see:
```
No user profile found. A profile can store default values for your projects.
Would you like to set up a profile now? [Y/n]: Y

LDA Profile Setup
----------------------------------------
This will set up default values for your projects.

Your name (for provenance tracking): Dr Jane Smith
Organization (optional): Research Institute  
Email (optional): jane.smith@institute.edu
Default language [python/r/both] (default: python): python

Profile saved to: ~/.config/lda/profile.yaml
You can edit this file anytime to update your defaults.
```

This creates `~/.config/lda/profile.yaml` with your defaults:
```yaml
defaults:
  analyst: "Dr Jane Smith"
  organization: "Research Institute"
  email: "jane.smith@institute.edu"
  language: "python"
```

You can also set up or update your profile anytime:
```bash
lda profile setup
```

## Creating Your First Project

### Interactive Structured Naming (Default)

LDA uses an interactive naming system by default to build consistent project names:

```bash
lda init
```

The system prompts you to use structured naming:
```
Would you like to use the structured naming system to build your project name? [Y/n]: Y

Let's build your project name
-----------------------------

1. Project/Study/Protocol (e.g., ALS301, COVID19, SensorX) [required]: ALS301
Preview: ALS301

2. Site/Organization/Consortium (e.g., US, LabA, UCL) [optional]: BOSTON
Preview: ALS301_BOSTON

3. Cohort/Arm/Group (e.g., Placebo, Elderly, Control) [optional]: Treatment
Preview: ALS301_BOSTON_Treatment

4. Phase/Session/Timepoint/Batch (e.g., 6mo, 2024A, Pre, Phase3) [optional]: 12mo
Preview: ALS301_BOSTON_Treatment_12mo

5. Modality/DataType/Task/Platform (e.g., MRI, RNAseq, Stroop, AWS) [optional]: Biomarkers
Preview: ALS301_BOSTON_Treatment_12mo_Biomarkers

6. Run/Version/Analysis/Config (e.g., v2, reanalysis, HighGain) [optional]: v1
Preview: ALS301_BOSTON_Treatment_12mo_Biomarkers_v1

7. Custom/Qualifier/Freeform (e.g., pilot, blinded, final) [optional]: 

Final Project Name
------------------
Preview: ALS301_BOSTON_Treatment_12mo_Biomarkers_v1

Is this correct? [Y/n]: Y

Project Configuration
---------------------
• Project Name: ALS301_BOSTON_Treatment_12mo_Biomarkers_v1
• Analyst: Dr Jane Smith
• Folder Name: ALS301_BOSTON_Treatment_12mo_Biomarkers_v1
• Organization: Research Institute
• Email: jane.smith@institute.edu

Is this correct? [Y/n]: Y

✨ Project created at: ALS301_BOSTON_Treatment_12mo_Biomarkers_v1/
```

Note: Project and site codes are automatically converted to uppercase for consistency.

### Using Naming Templates

Organizations can create templates for consistent naming:

```bash
# Use built-in clinical trial template
lda init --structured --naming-template templates/naming/clinical_trial.yaml

# Use custom template
lda init --structured --naming-template /path/to/custom_template.yaml
```

Example custom template:
```yaml
name: pharma_study
description: "Pharmaceutical study naming convention"

fields:
  - name: compound
    prompt: "Compound Code"
    examples: ["ABC123", "XYZ789"]
    required: true
    transform: upper
    
  - name: indication
    prompt: "Indication"
    examples: ["Alzheimer", "Parkinsons"]
    required: true
    
  - name: phase
    prompt: "Clinical Phase"
    examples: ["Phase1", "Phase2", "Phase3"]
    required: true
```


## Project Configuration

### Configuration File Structure

Each project has a YAML configuration file:

```yaml
project:
  name: "ALS301 Clinical Trial"
  code: "ALS301_BOS_Treatment"
  analyst: "Dr. Jane Smith"
  organization: "Boston Medical Center"
  email: "jane.smith@bmc.org"
  description: "Phase 3 clinical trial for ALS treatment"
  create_playground: true
  language: "python"

sections:
  - name: "01_data_collection"
    description: "Patient data collection and validation"
    language: "python"
    templates: ["clinical"]
    inputs:
      - "raw_data/*.csv"
      - "patient_info/*.xlsx"
    outputs:
      - "cleaned_data/*.csv"
      - "validation_report.pdf"
      
  - name: "02_statistical_analysis"
    description: "Primary and secondary endpoint analysis"
    language: "r"
    dependencies: ["01_data_collection"]
    inputs:
      - "../01_data_collection/cleaned_data/*.csv"
    outputs:
      - "results/*.csv"
      - "figures/*.png"
      - "statistical_report.pdf"
```

### Multi-Language Support

Configure sections with different languages:

```yaml
sections:
  - name: "python_analysis"
    language: "python"
    
  - name: "r_statistics"
    language: "r"
    
  - name: "mixed_processing"
    language: "both"  # Creates both run.py and run.R
```

### Advanced Configuration Options

```yaml
project:
  # Version control
  vcs:
    type: "git"
    auto_commit: false
    
  # File tracking
  tracking:
    auto_hash: true
    verify_checksums: true
    
  # Logging
  logging:
    level: "INFO"
    format: "detailed"
    
  # Naming conventions
  naming:
    style: "snake_case"
    date_format: "%Y%m%d"
```

## Working with Sections

### Creating Sections

Add sections to your configuration and sync:

```bash
# Edit config
vim ALS301_config.yaml

# Add sections
sections:
  - name: "01_screening"
    description: "Patient screening and enrollment"
    
  - name: "02_treatment"
    description: "Treatment administration and monitoring"
    
  - name: "03_analysis"
    description: "Statistical analysis of outcomes"

# Sync to create directories
lda sync
```

### Section Structure

Each section creates:
```
ALS301_BOS_Treatment/
├── ALS301_BOS_Treatment_sec01_screening/
│   ├── README.md
│   ├── run.py
│   ├── requirements.txt
│   ├── manifest.json
│   ├── inputs/
│   ├── outputs/
│   └── logs/
```

### Running Analysis in Sections

```bash
cd ALS301_BOS_Treatment_sec01_screening
python run.py
```

Or from project root:
```bash
lda run --section 01_screening
```

### Section Dependencies

Define execution order:

```yaml
sections:
  - name: "01_raw_data"
    
  - name: "02_preprocessing"
    dependencies: ["01_raw_data"]
    
  - name: "03_analysis"
    dependencies: ["02_preprocessing"]
    
  - name: "04_reporting"
    dependencies: ["02_preprocessing", "03_analysis"]
```

## File Tracking and Provenance

### Tracking Files

Track files in the project manifest:

```bash
# Track individual files
lda track data/patients.csv --section 01_screening --type input
lda track results/demographics.pdf --section 01_screening --type output

# Track with patterns
lda track "data/*.csv" --section 01_screening --type input

# Track with metadata
lda track results/analysis.csv \
  --section 03_analysis \
  --type output \
  --description "Primary endpoint analysis results" \
  --tags "primary,statistics"
```

### File Manifest

Each section maintains a manifest:

```json
{
  "files": {
    "inputs": {
      "patients.csv": {
        "hash": "sha256:abc123...",
        "size": 15420,
        "modified": "2024-11-30T10:30:00Z",
        "tracked": "2024-11-30T10:31:00Z",
        "analyst": "jane.smith",
        "provenance_id": "PROV-2024-1130-001"
      }
    },
    "outputs": {
      "demographics.pdf": {
        "hash": "sha256:def456...",
        "size": 245632,
        "modified": "2024-11-30T14:15:00Z",
        "tracked": "2024-11-30T14:16:00Z",
        "analyst": "jane.smith",
        "provenance_id": "PROV-2024-1130-002",
        "generated_from": ["patients.csv"],
        "script": "run.py",
        "version": "1.0"
      }
    }
  }
}
```

### Provenance Chain

Track complete data lineage:

```bash
# Show provenance for a file
lda provenance results/final_report.pdf

# Output:
Provenance Chain for: results/final_report.pdf
============================================

1. raw_data/patients.csv
   ↓ (01_screening/run.py v1.0)
2. cleaned_data/patients_screened.csv
   ↓ (02_preprocessing/run.py v1.2)
3. processed_data/patients_normalized.csv
   ↓ (03_analysis/run.py v2.0)
4. results/statistics.csv + figures/*.png
   ↓ (04_reporting/run.py v1.0)
5. results/final_report.pdf

Total transformation time: 4h 23m
Last updated: 2024-11-30 16:45:00
```

### Verification

Verify file integrity:

```bash
# Verify all tracked files
lda verify

# Verify specific section
lda verify --section 03_analysis

# Output:
Verifying tracked files...
✓ patients.csv (hash match)
✓ demographics.pdf (hash match)
✗ results.csv (hash mismatch - file modified)
  Expected: sha256:abc123...
  Actual: sha256:xyz789...
  
Verification complete: 2 passed, 1 failed
```

## Naming Conventions

### Structured Naming System

LDA enforces consistent naming through:

1. **Interactive field-based construction**
2. **Automatic case transformation**
3. **Template-based patterns**
4. **Validation rules**

### Field Transformations

Certain fields automatically convert case:

```yaml
fields:
  - name: protocol
    transform: upper  # ABC123 → ABC123, abc123 → ABC123
    
  - name: site
    transform: upper  # bos → BOS
    
  - name: visit
    transform: lower  # Week12 → week12
```

### File Naming Patterns

Configure file naming conventions:

```yaml
project:
  naming:
    # File naming pattern
    file_pattern: "{project}_{section}_{type}_{name}_{date}.{ext}"
    
    # Example: ALS301_sec01_input_patients_20241130.csv
    
    # Section naming pattern
    section_pattern: "{project}_sec{number}_{name}"
    
    # Example: ALS301_sec01_screening
```

### Custom Naming Rules

Add validation rules:

```yaml
project:
  validation:
    file_rules:
      - pattern: "^[A-Z0-9]+_"  # Must start with uppercase code
      - max_length: 255
      - forbidden: ["temp", "test", "tmp"]
    
    section_rules:
      - pattern: "^\d{2}_"  # Must start with 2-digit number
      - max_words: 3
```

## Advanced Features

### User Profiles

Set defaults for all projects:

```bash
# Setup profile
lda profile setup

# View current profile
lda profile show

# Update specific field
lda profile set analyst "Dr. Jane Smith"
lda profile set organization "New Institute"
```

Profile location: `~/.config/lda/profile.yaml`

### Environment Variables

Override settings with environment variables:

```bash
export LDA_ANALYST="Dr. Smith"
export LDA_ORGANIZATION="Research Lab"
export LDA_EMAIL="smith@lab.edu"
export LDA_LANGUAGE="r"

lda init --name "QuickProject"
```

### Template System

Create reusable project templates:

```bash
# Save current project as template
lda template save clinical_trial

# List available templates
lda template list

# Use template for new project
lda init --template clinical_trial --name "NewTrial"
```

Template structure:
```
templates/
├── clinical_trial/
│   ├── template.yaml
│   ├── file_patterns.yaml
│   ├── scripts/
│   │   ├── run_template.py
│   │   └── analysis_template.R
│   └── docs/
│       └── README_template.md
```

### Playground/Sandbox

Experimental work area:

```bash
cd MyProject/lda_playground

# Test new analysis
python experimental_analysis.py

# When ready, promote to section
lda promote experimental_analysis.py --to-section 02_analysis
```

### Git Integration

Automatic git tracking:

```yaml
project:
  vcs:
    type: "git"
    auto_commit: true
    commit_message_template: "LDA: {action} in {section}"
    
    # Creates commits like:
    # "LDA: Updated files in 01_screening"
    # "LDA: Added output demographics.pdf in 01_screening"
```

### Reporting

Generate project reports:

```bash
# Status report
lda report status --format pdf --output project_status.pdf

# Provenance report
lda report provenance --format html --output provenance_chain.html

# Compliance report
lda report compliance --standard "FDA" --output fda_compliance.pdf
```

## Best Practices

### 1. Project Organization

- Use structured naming for complex projects
- Keep sections focused on single analytical steps
- Number sections to indicate execution order
- Use descriptive section names

### 2. File Management

- Track files immediately after creation
- Use consistent file naming patterns
- Store raw data in read-only directories
- Keep processed data separate from raw data

### 3. Documentation

- Update section READMEs regularly
- Document data transformations in run scripts
- Include methodology in section descriptions
- Maintain a project-level CHANGELOG

### 4. Version Control

- Commit configuration changes immediately
- Use meaningful commit messages
- Tag stable analysis versions
- Branch for experimental work

### 5. Collaboration

- Share project templates with team
- Use consistent analyst names
- Document role responsibilities
- Regular sync meetings for multi-analyst projects

## Troubleshooting

### Common Issues

#### 1. Configuration Sync Fails

```bash
Error: Failed to sync configuration
```

Solution:
```bash
# Validate configuration
lda validate config

# Check for syntax errors
yamllint MyProject_config.yaml

# Force sync with backup
lda sync --force --backup
```

#### 2. File Tracking Issues

```bash
Error: File hash mismatch
```

Solution:
```bash
# Re-calculate hashes
lda track --recalculate

# Update specific file
lda track data/modified.csv --update --section 01_data

# Verify all files
lda verify --fix
```

#### 3. Naming Conflicts

```bash
Error: Project name already exists
```

Solution:
```bash
# Check existing projects
lda list projects

# Use different name or override
lda init --name "ProjectV2" --force
```

#### 4. Permission Issues

```bash
Error: Permission denied
```

Solution:
```bash
# Check file permissions
ls -la MyProject/

# Fix permissions
chmod -R u+rw MyProject/
```

### Debug Mode

Enable detailed logging:

```bash
# Run with debug output
lda --debug status

# Set debug in config
project:
  logging:
    level: "DEBUG"
    file: "lda_debug.log"
```

### Getting Help

1. **Built-in help**: `lda --help` or `lda <command> --help`
2. **Documentation**: `lda docs`
3. **GitHub Issues**: Report bugs at the repository
4. **Community Forum**: Discussion and questions

## Example: Complete Clinical Trial Workflow

Here's a real-world example of managing a clinical trial:

```bash
# 1. Initialize project with structured naming
lda init --structured

# Enter: Protocol: ABC123
#        Site: Boston
#        Phase: Phase3
#        Cohort: DrugArm

# 2. Configure sections
cat > ABC123_Boston_Phase3_DrugArm_config.yaml << EOF
project:
  name: "ABC123 Clinical Trial - Boston Site"
  code: "ABC123_Boston_Phase3_DrugArm"
  analyst: "Dr. Jane Smith"
  organization: "Boston Medical Center"

sections:
  - name: "01_patient_screening"
    description: "Initial patient screening and enrollment"
    inputs: ["screening_forms/*.pdf", "lab_results/*.csv"]
    outputs: ["eligible_patients.csv", "screening_report.pdf"]
    
  - name: "02_randomization"
    description: "Randomize patients to treatment arms"
    dependencies: ["01_patient_screening"]
    inputs: ["../01_patient_screening/eligible_patients.csv"]
    outputs: ["randomization_list.csv", "randomization_report.pdf"]
    
  - name: "03_treatment_phase"
    description: "Administer treatment and collect data"
    dependencies: ["02_randomization"]
    inputs: ["../02_randomization/randomization_list.csv"]
    outputs: ["treatment_data/*.csv", "adverse_events.csv"]
    
  - name: "04_statistical_analysis"
    description: "Analyze primary and secondary endpoints"
    dependencies: ["03_treatment_phase"]
    language: "r"
    inputs: ["../03_treatment_phase/treatment_data/*.csv"]
    outputs: ["statistical_results.csv", "figures/*.png", "stats_report.pdf"]
    
  - name: "05_final_report"
    description: "Generate final clinical trial report"
    dependencies: ["04_statistical_analysis"]
    inputs: ["../04_statistical_analysis/*"]
    outputs: ["final_report.pdf", "supplementary/*"]
EOF

# 3. Create project structure
lda sync

# 4. Work through sections
cd ABC123_Boston_Phase3_DrugArm_sec01_patient_screening

# Add screening data
cp /source/screening/*.pdf inputs/
lda track "inputs/*.pdf" --type input

# Run screening analysis
python run.py

# Track outputs
lda track outputs/eligible_patients.csv --type output

# 5. Continue through workflow
cd ../ABC123_Boston_Phase3_DrugArm_sec02_randomization
# ... continue process

# 6. Generate final reports
lda report status --format pdf
lda report provenance --output provenance_report.html

# 7. Archive completed project
lda archive --compress --validate
```

## Conclusion

LDAnalysis provides comprehensive project management for research workflows. Key benefits include:

- **Complete Provenance**: Track every file and transformation
- **Structured Organization**: Consistent project layouts
- **Flexible Configuration**: Adapt to any workflow
- **Multi-language Support**: Use Python, R, or both
- **Validation & Verification**: Ensure data integrity
- **Collaborative Features**: Team-friendly defaults

Start with simple projects and gradually adopt advanced features as needed. The system grows with your requirements while maintaining simplicity for basic use cases.

For the latest updates and features, visit the [LDAnalysis GitHub repository](https://github.com/cincineuro/ldanalysis).