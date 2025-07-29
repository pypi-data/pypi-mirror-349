# Strict Mode and Validation

As of LDA v0.2.0, strict validation is enabled by default for the `init` command. This ensures data quality and proper provenance tracking.

## What is Strict Mode?

Strict mode enforces:
- Required fields must be provided (no silent defaults)
- Input validation for all values
- Proper naming conventions
- Interactive confirmation when available

## Required Fields

When initializing a project, you must provide:
- **Project Name** (`--name`): The human-readable project name
- **Analyst Name** (`--analyst`): The person responsible for the project

```bash
# Correct usage (strict mode is default)
lda init --name "Climate Study 2024" --analyst "jane.doe"

# This will fail with an error
lda init  # Missing required fields
```

## Using User Profiles

To avoid typing the same values repeatedly, set up a user profile:

```bash
# Interactive profile setup
lda profile setup

# Or set individual values
lda profile set defaults.analyst "jane.doe"
lda profile set defaults.organization "Research Lab"
lda profile set defaults.email "jane@lab.edu"
```

Profile values are used as defaults but can be overridden:

```bash
# Uses analyst from profile
lda init --name "New Study"

# Overrides profile analyst
lda init --name "New Study" --analyst "john.smith"
```

## Environment Variables

For CI/CD or automated environments:

```bash
export LDA_ANALYST="ci-bot"
export LDA_ORGANIZATION="AutomatedTests"

lda init --name "Test Project"
```

## Value Priority

Values are resolved in this order (highest to lowest):
1. Command line arguments
2. Environment variables
3. User profile defaults
4. Interactive prompts (if TTY)
5. Error if required value missing

## Smart Name Parsing

LDA can extract metadata from structured project names:

```bash
lda init --name "Smith_ALS301_2024"

# Detects:
# - Analyst: smith
# - Code: ALS301
# - Date: 2024
```

You'll be asked to confirm extracted values in interactive mode.

## Validation Rules

### Project Names
- 3-100 characters long
- Must start with letter or number
- Only letters, numbers, spaces, underscores, hyphens
- Cannot use reserved words (test, docs, config, etc.)

### Analyst Names
- 2-50 characters long
- Must start with a letter
- Only letters, numbers, dots, underscores, hyphens, spaces

### Section Names
- 2-50 characters long
- Must start with a letter
- Only letters, numbers, underscores, hyphens

## Legacy Mode (Deprecated)

For backward compatibility, you can temporarily use legacy mode:

```bash
lda init --legacy
```

⚠️ **Warning**: Legacy mode is deprecated and will be removed in v0.3.0.

## Migration Guide

If you're upgrading from an older version:

1. Update scripts to include required fields:
   ```bash
   # Old (will fail)
   lda init
   
   # New (required)
   lda init --name "Project Name" --analyst "your.name"
   ```

2. Set up a profile for convenience:
   ```bash
   lda profile setup
   ```

3. Update CI/CD pipelines:
   ```yaml
   - name: Initialize Project
     env:
       LDA_ANALYST: github-actions
     run: |
       lda init --name "${{ github.event.repository.name }}"
   ```

## Interactive Mode

When running in a terminal, LDA provides helpful prompts:

```bash
$ lda init --name "Climate Study"
LDA Project Initialization
==========================

No user profile found. Would you like to set up a profile now? [Y/n]: y

LDA Profile Setup
-----------------
Your name (for provenance tracking): jane.doe
Organization (optional): Climate Research Lab
Email (optional): jane@lab.edu

Profile saved to: ~/.config/lda/profile.yaml

Project Configuration
--------------------
• Name: Climate Study
• Analyst: jane.doe

Is this correct? [Y/n]: y
```

## Error Messages

Strict mode provides clear, actionable error messages:

```
Validation Error: name
----------------------------------------
Project name must be at least 3 characters long

Provided value: 'AB'

Project names must:
- Be 3-100 characters long
- Start with a letter or number
- Contain only letters, numbers, spaces, underscores, and hyphens
- Not use reserved words (test, docs, config, etc.)
```

## Best Practices

1. **Always set up a profile**: Reduces typing and ensures consistency
2. **Use meaningful project names**: They become folder names and identifiers
3. **Include metadata in names**: Helps with automatic extraction
4. **Validate early**: Fix issues before creating project structure
5. **Document conventions**: Create naming standards for your team

## FAQ

**Q: How do I disable strict mode?**
A: Use `--legacy` flag, but this is deprecated and will be removed.

**Q: Can I change project metadata after creation?**
A: Edit the `{project}_config.yaml` file and run `lda sync`.

**Q: What if I forget the analyst name?**
A: You'll be prompted interactively, or use `lda profile show` to check.

**Q: How do I handle multiple analysts?**
A: Use the primary analyst for init, document others in the project.