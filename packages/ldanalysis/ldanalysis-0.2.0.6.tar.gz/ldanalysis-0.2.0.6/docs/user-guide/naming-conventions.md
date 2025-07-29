# Naming Conventions

LDA provides flexible naming conventions for projects while maintaining filesystem compatibility. The system now includes an interactive structured naming system that guides you through building project names using field-based components.

## Interactive Structured Naming (New)

When creating a new project, you can use the structured naming system to build your project name interactively:

```bash
lda init --structured
```

This will guide you through a series of prompts to build your project name:

```
Let's build your project name:

1. Project/Study/Protocol (e.g., ALS301, COVID19, SensorX) [required]: ALS301
2. Site/Organization/Consortium (e.g., US, LabA, UCL) [optional]: US
3. Cohort/Arm/Group (e.g., Placebo, Elderly) [optional]: Placebo
4. Phase/Session/Timepoint/Batch (e.g., 6mo, 2024A, Pre) [optional]: 6mo
5. Modality/DataType/Task/Platform (e.g., MRI, RNAseq, Stroop) [optional]: MRI
6. Run/Version/Analysis/Config (e.g., v2, reanalysis, HighGain) [optional]: [skip]
7. Custom/Qualifier/Freeform (e.g., pilot, blinded) [optional]: [skip]

Preview: ALS301_US_Placebo_6mo_MRI
Is this correct? [Y/n]: Y
```

### Field Structure

The naming system uses the following fields (in order):

1. **Project/Study/Protocol** (required)
   - The primary identifier for your project
   - Examples: `ALS301`, `COVID19`, `SensorX`

2. **Site/Organization/Consortium** (optional)
   - Location or organizational identifier
   - Examples: `US`, `LabA`, `UCL`

3. **Cohort/Arm/Group** (optional)
   - Study group or treatment arm
   - Examples: `Placebo`, `Elderly`, `Control`

4. **Phase/Session/Timepoint/Batch** (optional)
   - Temporal or batch identifier
   - Examples: `6mo`, `2024A`, `Pre`, `Phase3`

5. **Modality/DataType/Task/Platform** (optional)
   - Type of data or experimental condition
   - Examples: `MRI`, `RNAseq`, `Stroop`, `AWS`

6. **Run/Version/Analysis/Config** (optional)
   - Specific run or configuration
   - Examples: `v2`, `reanalysis`, `HighGain`

7. **Custom/Qualifier/Freeform** (optional)
   - Any additional qualifiers
   - Examples: `pilot`, `blinded`, `final`

## Traditional Naming

You can still provide project names directly:

```bash
lda init --name "CN111_SPG302_REST_WK8"
```

## Project Names vs Project Codes

- **Project Name**: The human-readable name you provide (e.g., "CN111_SPG302_REST_WK8")
- **Project Code**: The folder name derived from the project name

By default, LDA preserves your project name as the folder name, making it intuitive to navigate.

## Default Behavior

When you create a project:

```bash
lda init --name "CN111_SPG302_REST_WK8"
```

This creates:
- Folder: `CN111_SPG302_REST_WK8/`
- Config: `CN111_SPG302_REST_WK8_config.yaml`

The full project name is preserved for intuitive navigation.

## Automatic Sanitization

LDA automatically sanitizes project names for filesystem compatibility:

- Removes problematic characters: `< > : " / \ | ? *`
- Replaces spaces with underscores
- Preserves underscores and hyphens
- Maintains uppercase and lowercase

## Case Transformation

Certain fields can be automatically transformed for consistency:

- Project codes and site codes are converted to uppercase by default
- Use `transform: upper` in templates to enforce uppercase
- Use `transform: lower` for lowercase conversion
- Leave out `transform` to preserve original case

Example:
- Input: "spg302" → Output: "SPG302"
- Input: "cn111" → Output: "CN111"

Examples:
```
"My Research Project" → "My_Research_Project"
"Study: Phase 3" → "Study_Phase_3"
"Data/Analysis" → "DataAnalysis"
```

## Scientific Naming Patterns

LDA recognizes common scientific naming patterns:

### Clinical Trial Pattern
```
CN111_SPG302_REST_WK8
├── Site: CN111
├── Study: SPG302
├── Condition: REST
└── Week: WK8
```

### Research Study Pattern
```
Smith_ALS301_2024Q1
├── Analyst: Smith
├── Study: ALS301
└── Period: 2024Q1
```

### Phase Study Pattern
```
Alzheimer_Phase3_2024
├── Condition: Alzheimer
├── Phase: 3
└── Year: 2024
```

## Using Naming Templates

Organizations can create custom naming templates to match their conventions. Templates are YAML files that define field structure and requirements.

### Using a Template

```bash
lda init --structured --naming-template /path/to/template.yaml
```

### Built-in Templates

LDA includes several pre-configured templates:

- **clinical_trial.yaml** - For clinical research projects
- **data_science.yaml** - For machine learning and data science projects
- **academic_research.yaml** - For academic research projects
- **engineering.yaml** - For software engineering projects

### Creating Custom Templates

Create a YAML file with the following structure:

```yaml
name: my_template
description: "Custom naming convention for my organization"

fields:
  - name: project
    prompt: "Project Code"
    examples: ["PROJ001", "EXP2024"]
    required: true
    transform: upper  # Automatically converts to uppercase
    
  - name: department
    prompt: "Department/Lab"
    examples: ["NeuroBio", "CompSci"]
    required: true
    aliases: ["lab", "group"]
    
  - name: phase
    prompt: "Research Phase"
    examples: ["Pilot", "Main", "Followup"]
    required: false

required_fields: 
  - project
  - department

field_order:
  - project
  - department
  - phase
```

## Custom Project Codes

You can override the automatic code generation:

```bash
lda init --name "Long Descriptive Project Name" --code "LDPN"
```

This creates:
- Folder: `LDPN/`
- Config: `LDPN_config.yaml`

## Best Practices

1. **Use Consistent Patterns**: Adopt a naming convention for your organization
2. **Include Metadata**: Embed study codes, dates, and conditions in names
3. **Avoid Special Characters**: Stick to letters, numbers, underscores, and hyphens
4. **Be Descriptive**: Names should be self-documenting

## Examples

Good naming examples:
- `CN111_SPG302_REST_WK8`
- `Smith_DrugStudy_2024`
- `ALS301_Boston_2024Q1`
- `MRI_Analysis_Phase2`

These names:
- Are self-documenting
- Work across all operating systems
- Sort well alphabetically
- Contain embedded metadata

## Configuration

You can configure naming behavior in your profile:

```yaml
# ~/.config/lda/profile.yaml
defaults:
  naming_style: "preserve"  # or "compact"
  auto_detect_metadata: true
```

Options:
- `preserve`: Keep full project name as folder name (default)
- `compact`: Generate short codes from project names

## Changing Project Names

To rename a project after creation:

1. Edit the config file
2. Rename the folder
3. Run `lda sync` to update references

```bash
# Edit the config
vim CN111_SPG302_REST_WK8_config.yaml

# Rename the folder
mv CN111_SPG302_REST_WK8 CN111_SPG302_REST_WK12

# Update references
lda sync
```

## Manual Override

You can always override the structured naming system and enter a custom name:

1. When prompted "Is this correct?", answer `n`
2. You'll be asked: "Enter custom project name (or press Enter to rebuild):"
3. Enter your custom name or press Enter to start over

## Hierarchical Projects

For complex projects with many fields, the system may suggest a hierarchical folder structure:

```
ALS301/
├── US/
│   ├── Placebo/
│   │   ├── 6mo/
│   │   │   └── MRI/
```

This can be useful for organizing deeply nested research projects.

## Command Line Options

- `--structured`: Use the interactive naming system
- `--naming-template <path>`: Use a specific naming template
- `--name <name>`: Provide the full name directly (bypasses structured naming)

## Validation Rules

Project names must:
- Be 3-100 characters long
- Start with a letter or number
- Contain only letters, numbers, spaces, underscores, and hyphens
- Not use reserved words (test, docs, config, etc.)

The system will provide clear error messages if validation fails.

## FAQ

**Q: What if my project doesn't fit the field structure?**
A: Use the custom field for additional qualifiers, or provide a completely custom name when prompted.

**Q: Can I change field labels?**
A: Yes, create a custom template with your preferred field names and prompts.

**Q: Are all fields required?**
A: Only the first field (Project/Study/Protocol) is required by default. You can customize this in templates.

**Q: How do I handle multiple sites or arms?**
A: You can include multiple values in a single field (e.g., "US-EU" for sites) or create separate projects for each combination.

**Q: Can I use special characters?**
A: The system automatically sanitizes names for filesystem compatibility. Spaces become underscores, and forbidden characters are removed.

**Q: When should I use structured naming vs traditional naming?**
A: Use structured naming when you have complex projects with multiple components. Use traditional naming for simple projects or when you have an existing naming convention.