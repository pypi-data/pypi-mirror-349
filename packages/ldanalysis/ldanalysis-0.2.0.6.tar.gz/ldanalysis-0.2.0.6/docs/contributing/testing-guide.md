# Testing Guide

This guide covers how to run tests for the LDA project, write new tests, and understand our testing infrastructure.

## Prerequisites

Before running tests, ensure you have the development dependencies installed:

```bash
# Using uv (recommended)
uv pip install -e ".[dev]"

# Or using pip
pip install -e ".[dev]"
```

This installs pytest and other testing tools needed for running the test suite.

## Running Tests

### Run All Tests

To run the complete test suite:

```bash
pytest
```

### Run Tests with Coverage

To see test coverage reports:

```bash
pytest --cov=lda --cov-report=term-missing
```

This will show:
- Which files are tested
- Line-by-line coverage
- Missing lines that need tests

### Run Specific Test Files

```bash
# Run a single test file
pytest tests/test_validation.py

# Run multiple specific files
pytest tests/test_validation.py tests/test_profile.py
```

### Run Tests by Pattern

```bash
# Run all validation tests
pytest -k validation

# Run all tests containing "profile" in name
pytest -k profile

# Exclude tests with "slow" marker
pytest -m "not slow"
```

### Verbose Output

For more detailed test output:

```bash
pytest -vv
```

## Test Organization

Tests are organized by module:

```
tests/
├── conftest.py          # Shared fixtures
├── test_basic.py        # Basic functionality tests
├── test_cli.py          # CLI command tests
├── test_config.py       # Configuration tests
├── test_init_features.py # New init command tests
├── test_validation.py   # Input validation tests
├── test_name_parser.py  # Smart name parsing tests
├── test_profile.py      # User profile tests
├── test_interactive.py  # Interactive prompt tests
├── test_deprecation.py  # Deprecation handling tests
└── unit/               # Unit tests
    ├── test_config.py
    ├── test_errors.py
    ├── test_manifest.py
    ├── test_scaffold.py
    └── test_tracking.py
```

## Writing Tests

### Test Structure

Follow this pattern for test classes and methods:

```python
import pytest
from lda.core.validation import ProjectValidator


class TestProjectValidator:
    """Test project validation rules."""
    
    def test_validate_project_name_valid(self):
        """Test valid project names."""
        valid_names = ["Project 2024", "Research_Study"]
        
        for name in valid_names:
            is_valid, error = ProjectValidator.validate_project_name(name)
            assert is_valid, f"'{name}' should be valid: {error}"
    
    def test_validate_project_name_invalid(self):
        """Test invalid project names."""
        invalid_cases = [
            ("", "Project name cannot be empty"),
            ("ab", "Project name must be at least 3 characters"),
        ]
        
        for name, expected_error in invalid_cases:
            is_valid, error = ProjectValidator.validate_project_name(name)
            assert not is_valid
            assert expected_error in error
```

### Using Fixtures

Common fixtures are in `conftest.py`:

```python
@pytest.fixture
def temp_project(tmp_path):
    """Create a temporary project structure."""
    project_dir = tmp_path / "test_project"
    project_dir.mkdir()
    return project_dir


def test_with_fixture(temp_project):
    """Test using the fixture."""
    assert temp_project.exists()
```

### Mocking External Dependencies

Use unittest.mock for testing interactions:

```python
from unittest.mock import Mock, patch


@patch('builtins.input', return_value='y')
def test_user_confirmation(mock_input):
    """Test user input handling."""
    result = confirm_action("Continue?")
    assert result is True
    mock_input.assert_called_once()
```

## Running Specific Test Types

### Unit Tests Only

```bash
pytest tests/unit/
```

### Integration Tests

```bash
pytest tests/integration/
```

### Tests with Specific Markers

```bash
# Run only fast tests
pytest -m "not slow"

# Run only integration tests
pytest -m integration
```

## Test Coverage Goals

We aim for:
- Overall coverage: >80%
- Core modules: >90%
- New features: 100%

Check current coverage:

```bash
pytest --cov=lda --cov-report=html
open htmlcov/index.html
```

## Debugging Tests

### Run with Python Debugger

```bash
pytest --pdb
```

This drops into the debugger on test failure.

### Run with Detailed Output

```bash
pytest -vv --tb=long
```

### Run Single Test

```bash
pytest tests/test_validation.py::TestProjectValidator::test_validate_project_name_valid
```

## Continuous Integration

Tests run automatically on:
- Every push to main
- Every pull request
- Nightly builds

See `.github/workflows/test.yml` for CI configuration.

## Test Best Practices

1. **Write tests first**: Follow TDD when possible
2. **One assertion per test**: Keep tests focused
3. **Clear test names**: Describe what's being tested
4. **Use fixtures**: DRY principle for test setup
5. **Mock external dependencies**: Tests should be isolated
6. **Test edge cases**: Empty inputs, None values, etc.
7. **Test error paths**: Ensure errors are handled properly

## Common Testing Patterns

### Testing CLI Commands

```python
def test_init_command_strict_mode(capsys):
    """Test init command with strict mode."""
    from lda.cli.main import LDACLI
    
    cli = LDACLI()
    result = cli.run(["init", "--name", "Test", "--analyst", "user", "--strict"])
    
    captured = capsys.readouterr()
    assert result == 0
    assert "Project created" in captured.out
```

### Testing File Operations

```python
def test_file_creation(tmp_path):
    """Test that files are created correctly."""
    config_file = tmp_path / "config.yaml"
    
    # Create file
    config = LDAConfig()
    config.save(str(config_file))
    
    # Verify
    assert config_file.exists()
    assert config_file.read_text().startswith("project:")
```

### Testing Validation

```python
def test_email_validation():
    """Test email validation patterns."""
    test_cases = [
        ("user@example.com", True),
        ("invalid", False),
        ("", True),  # Empty is valid (optional)
    ]
    
    for email, expected in test_cases:
        is_valid, _ = validate_email(email)
        assert is_valid == expected
```

## Troubleshooting

### Import Errors

If you get import errors, ensure LDA is installed in development mode:

```bash
uv pip install -e .
```

### Fixture Not Found

Make sure `conftest.py` is in the tests directory and contains the fixture.

### Tests Not Discovered

Ensure test files start with `test_` and test functions start with `test_`.

### Coverage Not Working

Install coverage tools:

```bash
uv pip install pytest-cov
```

## Adding New Tests

When adding new features:

1. Create a test file: `tests/test_new_feature.py`
2. Write tests covering:
   - Normal operation
   - Edge cases
   - Error conditions
3. Run tests: `pytest tests/test_new_feature.py`
4. Check coverage: `pytest --cov=lda.module tests/test_new_feature.py`
5. Commit tests with feature code

## Test Data

Test data is stored in `tests/fixtures/` directory. Use it for:
- Sample configuration files
- Mock project structures
- Test input/output files

```python
def test_with_fixture_data():
    """Test using fixture data."""
    fixture_path = Path(__file__).parent / "fixtures" / "sample_config.yaml"
    config = LDAConfig(str(fixture_path))
    assert config.get("project.name") == "Test Project"
```

## Next Steps

- Read about [Development Workflow](development.md)
- Learn about [Contributing](../contributing.md)
- Check [CI/CD Pipeline](ci-cd.md)