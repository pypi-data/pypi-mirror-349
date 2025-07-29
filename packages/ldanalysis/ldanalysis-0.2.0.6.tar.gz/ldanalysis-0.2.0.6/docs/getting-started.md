# Getting Started with LDA

This guide walks you through the essential first steps with LDA, from checking your installation to creating and managing your first project.

## Installation Check

First, verify that LDA is properly installed and check which version you're using:

```bash
lda --version
```

Output:
```
LDAnalysis version 0.2.0.1
```

## Exploring Available Commands

To see all available commands and options:

```bash
lda --help
```

Output:
```
LDAnalysis - Linked Document Analysis

Usage:
  lda [options] <command> [command-options]

Commands:
  init      Create a new LDA project
  status    Show project status
  sync      Synchronize project with config
  track     Track files in manifest
  profile   Manage user profile
  docs      Documentation tools
  version   Show version information

Options:
  -h, --help     Show this help message
  -v, --verbose  Enable verbose output
  -q, --quiet    Suppress all output except errors
  --config FILE  Specify config file

Run 'lda <command> --help' for more information on a command.
```

## Setting Up Your Profile

Setting up a user profile allows LDA to use consistent information across projects:

```bash
lda profile setup
```

Interactive output:
```
LDA Profile Setup
----------------------------------------
This will set up default values for your projects.

Your name (for provenance tracking): Jane Smith
Organization (optional): Research Institute
Email (optional): jane.smith@research.org
Default language [python/r/both] (default: python): python

Profile saved to: ~/.config/lda/profile.yaml
You can edit this file anytime to update your defaults.
```

## Creating Your First Project

Now let's create a new project:

```bash
lda init
```

Interactive output:
```
LDA Project Initialization
============================================================
Would you like to use the structured naming system to build your project name? [Y/n]: Y

Let's build your project name
-----------------------------

1. Project/Study/Protocol (e.g., ALS301, COVID19, SensorX) [required]: SPG302
Preview: SPG302

2. Site/Organization/Consortium (e.g., US, LabA, UCL) [optional]: CN
Preview: SPG302_CN

3. Cohort/Arm/Group (e.g., Placebo, Elderly, Control) [optional]: ALS
Preview: SPG302_CN_ALS

4. Phase/Session/Timepoint/Batch (e.g., 6mo, 2024A, Pre, Phase3) [optional]: WK24
Preview: SPG302_CN_ALS_WK24

5. Modality/DataType/Task/Platform (e.g., MRI, RNAseq, Stroop, AWS) [optional]: EEG
Preview: SPG302_CN_ALS_WK24_EEG

6. Run/Version/Analysis/Config (e.g., v2, reanalysis, HighGain) [optional]: REST
Preview: SPG302_CN_ALS_WK24_EEG_REST

7. Custom/Qualifier/Freeform (e.g., pilot, blinded, final) [optional]: 

Final Project Name
------------------
Preview: SPG302_CN_ALS_WK24_EEG_REST

Is this correct? [Y/n]: Y

Project Configuration
---------------------
• Project Name: SPG302_CN_ALS_WK24_EEG_REST
• Analyst: Jane Smith
• Organization: Research Institute
• Email: jane.smith@research.org
• Folder Name: SPG302_CN_ALS_WK24_EEG_REST

Is this correct? [Y/n]: Y

✨ Project created at: SPG302_CN_ALS_WK24_EEG_REST/
📋 Sections created: []
📁 Playground created: lda_playground/
📄 Files created: 1
💾 Configuration saved: SPG302_CN_ALS_WK24_EEG_REST/lda_config.yaml
⏱️ Time taken: 0.12s

Next Steps
----------
• cd SPG302_CN_ALS_WK24_EEG_REST
• lda status  # Check project status
• lda track <file> --section name --type input  # Track input files
```

## Navigating to Your Project

Change to your project directory:

```bash
cd SPG302_CN_ALS_WK24_EEG_REST
```

## Adding Sections to Your Project

Let's add analysis sections to your project by editing the configuration file:

```bash
# Open the config file in your favorite editor
nano lda_config.yaml
```

Add sections to the configuration:

```yaml
# Add this under the existing content
sections:
  - name: "preprocessing"
    description: "Data cleaning and normalization"
    inputs: ["raw_data/*.csv"]
    outputs: ["processed_data.csv"]
  
  - name: "analysis"
    description: "Statistical analysis"
    inputs: ["../preprocessing/processed_data.csv"]
    outputs: ["results/*.csv", "figures/*.png"]
```

## Syncing Your Project

After editing the configuration, sync your project to create the new sections:

```bash
lda sync
```

Output:
```
LDA Project Sync
============================================================
INFO: Loaded configuration from: /path/to/SPG302_CN_ALS_WK24_EEG_REST/lda_config.yaml
SUCCESS: Created section: preprocessing
SUCCESS: Created section: analysis
SUCCESS: Updated project files
```

## Checking Project Status

View your project's current status:

```bash
lda status
```

Output:
```
Project Status
============================================================
Project Information
---------------------
Name: SPG302_CN_ALS_WK24_EEG_REST
Code: SPG302_CN_ALS_WK24_EEG_REST
Analyst: Jane Smith
Created: 2024-05-20T10:30:00
Root: /path/to/SPG302_CN_ALS_WK24_EEG_REST

Summary
---------------------
Sections: 2
Total files: 0
Input files: 0
Output files: 0
Last activity: 2024-05-20T10:30:00

Sections
---------------------
preprocessing:
  Folder: SPG302_CN_ALS_WK24_EEG_REST_secpreprocessing
  Created: 2024-05-20T10:35:00
  Provenance: PROV-20240520-001

analysis:
  Folder: SPG302_CN_ALS_WK24_EEG_REST_secanalysis
  Created: 2024-05-20T10:35:00
  Provenance: PROV-20240520-002
```

## Project Structure

Your project now has this structure:

```
SPG302_CN_ALS_WK24_EEG_REST/
├── lda_config.yaml
├── lda_manifest.csv
├── README.md
├── .lda/
│   └── config.yaml
├── lda_playground/
│   ├── experiments/
│   ├── notebooks/
│   └── scratch/
├── SPG302_CN_ALS_WK24_EEG_REST_secpreprocessing/
│   ├── README.md
│   ├── run.py
│   ├── inputs/
│   ├── outputs/
│   └── logs/
└── SPG302_CN_ALS_WK24_EEG_REST_secanalysis/
    ├── README.md
    ├── run.py
    ├── inputs/
    ├── outputs/
    └── logs/
```

## What's Next

Now that you have your project set up, you can:

1. Add input data files to your section input folders
2. Track files in your project with `lda track`
3. Run analysis scripts with `python run.py` in each section folder
4. Check the status of your project with `lda status`
5. Expand your project with more sections using `lda sync`

This barebones tutorial gives you the essential commands to get started with LDA. As you become more familiar with the system, you can explore advanced features like file tracking, provenance chains, and custom naming templates.