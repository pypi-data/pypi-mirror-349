# LDAnalysis (LDA)

A provenance-driven project management system that creates a living map of your research, tracking relationships, monitoring changes, and preserving your project's complete history.

Each analysis folder, manifest, and result is named and organized to mirror the document outline, creating a one-to-one link between text, code, data, and results.

This architecture ensures that every figure, table, or claim in the document is transparently and immutably traceable back to its generating code and data—enabling instant audit, replication, and regulatory review.

## Installation

### Quick Install (Recommended)

Install using [UV](https://github.com/astral-sh/uv) for a fast, isolated global installation:

```bash
# Install UV (one-time setup)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install LDAnalysis
uv tool install ldanalysis
```

### Alternative Method

Using pipx:
```bash
pipx install ldanalysis
```

### Development Installation

For contributors or to use the development version:
```bash
# Clone the repository
git clone https://github.com/cincineuro/ldanalysis.git

# Install with UV in development mode
uv tool install --upgrade -e /path/to/ldanalysis
```

For detailed installation instructions, see the [Installation Guide](https://cincineuro.github.io/ldanalysis/installation/).

**Requirements**: Python 3.8 or later

## Quick Start

### First-Time Setup

When you first run LDA, you'll be prompted to create a profile:

```bash
lda init
```

```
No user profile found. A profile can store default values for your projects.
Would you like to set up a profile now? [Y/n]: Y

Your name (for provenance tracking): Dr Jane Smith
Organization (optional): Research Institute
Email (optional): jane.smith@institute.edu
Default language [python/r/both] (default: python): python

Profile saved to: ~/.config/lda/profile.yaml
```

### Create a Project

LDA uses an interactive naming system to build structured project names:

```bash
lda init
```

```
Would you like to use the structured naming system? [Y/n]: Y

Let's build your project name
-----------------------------
1. Project/Study/Protocol (e.g., ALS301, COVID19, SensorX) [required]: ALS301
2. Site/Organization/Consortium (e.g., US, LabA, UCL) [optional]: CCHMC
3. Cohort/Arm/Group (e.g., Placebo, Elderly, Control) [optional]: Treatment
4. Phase/Session/Timepoint/Batch (e.g., 6mo, 2024A, Pre) [optional]: Week8
5. Modality/DataType/Task/Platform (e.g., MRI, RNAseq, Stroop) [optional]: EEG

Preview: ALS301_CCHMC_Treatment_Week8_EEG

Is this correct? [Y/n]: Y

✨ Project created: ALS301_CCHMC_Treatment_Week8_EEG/
```

The tool will:
1. Create a project with structured naming
2. Set up section folders for your analysis
3. Generate file manifests for tracking
4. Initialize provenance with unique IDs
5. Create a playground for experimentation

## Project Structure

Each LDA project contains:
- **Section folders**: One-to-one mapping with document sections
- **File manifests**: Explicit lists of expected inputs and outputs
- **Provenance tracking**: Hashes, timestamps, and analyst attribution
- **Audit logs**: Complete history of all changes

## Documentation

See [CLAUDE.md](CLAUDE.md) for detailed architecture and usage instructions.

## License

MIT License - see LICENSE file for details.