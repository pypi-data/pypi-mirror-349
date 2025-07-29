"""Test validation functionality."""

import pytest
from lda.core.validation import ProjectValidator


class TestProjectValidator:
    """Test project validation rules."""
    
    def test_validate_project_name_valid(self):
        """Test valid project names."""
        valid_names = [
            "Climate Study 2024",
            "Drug_Trial_Phase3",
            "ALS-301-Analysis",
            "MyProject123",
            "Research_2024",
            "Simple Name"
        ]
        
        for name in valid_names:
            is_valid, error = ProjectValidator.validate_project_name(name)
            assert is_valid, f"'{name}' should be valid: {error}"
    
    def test_validate_project_name_invalid(self):
        """Test invalid project names."""
        invalid_cases = [
            ("", "Project name cannot be empty"),
            ("  ", "Project name cannot be empty"),
            ("ab", "Project name must be at least 3 characters long"),
            ("a" * 101, "Project name must be less than 100 characters"),
            ("test", "'test' is a reserved word"),
            ("docs", "'docs' is a reserved word"),
            ("..", "'..' is a system path"),
            ("project@home", "can only contain letters, numbers, spaces, underscores, and hyphens"),
            ("#project", "Project name must start with a letter or number"),
            ("_project", "Project name must start with a letter or number"),
        ]
        
        for name, expected_error in invalid_cases:
            is_valid, error = ProjectValidator.validate_project_name(name)
            assert not is_valid
            assert expected_error in error
    
    def test_validate_analyst_name_valid(self):
        """Test valid analyst names."""
        valid_names = [
            "john.doe",
            "jane_smith",
            "Dr Smith",
            "user123",
            "Mary-Jane",
            "Test User"
        ]
        
        for name in valid_names:
            is_valid, error = ProjectValidator.validate_analyst_name(name)
            assert is_valid, f"'{name}' should be valid: {error}"
    
    def test_validate_analyst_name_invalid(self):
        """Test invalid analyst names."""
        invalid_cases = [
            ("", "Analyst name cannot be empty"),
            ("a", "Analyst name must be at least 2 characters long"),
            ("a" * 51, "Analyst name must be less than 50 characters"),
            ("user@domain", "can only contain letters, numbers, dots, underscores, hyphens, and spaces"),
            ("123user", "Analyst name must start with a letter"),
            (".user", "Analyst name must start with a letter"),
        ]
        
        for name, expected_error in invalid_cases:
            is_valid, error = ProjectValidator.validate_analyst_name(name)
            assert not is_valid
            assert expected_error in error
    
    def test_validate_project_code_valid(self):
        """Test valid project codes."""
        valid_codes = [
            "ALS301",
            "DRUG_2024",
            "Code123",
            "MyCode",
            "TEST_01"
        ]
        
        for code in valid_codes:
            is_valid, error = ProjectValidator.validate_project_code(code)
            assert is_valid, f"'{code}' should be valid: {error}"
    
    def test_validate_project_code_invalid(self):
        """Test invalid project codes."""
        invalid_cases = [
            ("", "Project code cannot be empty"),
            ("a", "Project code must be at least 2 characters long"),
            ("a" * 21, "Project code must be less than 20 characters"),
            ("code-123", "can only contain letters, numbers, and underscores"),
            ("123code", "Project code must start with a letter"),
            ("_code", "Project code must start with a letter"),
            ("test", "'test' is a reserved word"),
        ]
        
        for code, expected_error in invalid_cases:
            is_valid, error = ProjectValidator.validate_project_code(code)
            assert not is_valid
            assert expected_error in error
    
    def test_validate_email_valid(self):
        """Test valid email addresses."""
        valid_emails = [
            "user@example.com",
            "john.doe@company.org",
            "test123@mail.co.uk",
            "user+tag@domain.com",
            "",  # Empty email is valid (optional field)
        ]
        
        for email in valid_emails:
            is_valid, error = ProjectValidator.validate_email(email)
            assert is_valid, f"'{email}' should be valid: {error}"
    
    def test_validate_email_invalid(self):
        """Test invalid email addresses."""
        invalid_emails = [
            "invalid",
            "@domain.com",
            "user@",
            "user@domain",
            "user domain@example.com",
        ]
        
        for email in invalid_emails:
            is_valid, error = ProjectValidator.validate_email(email)
            assert not is_valid
    
    def test_validate_section_name_valid(self):
        """Test valid section names."""
        valid_names = [
            "data",
            "analysis",
            "results",
            "preprocessing",
            "model_training",
            "phase-1"
        ]
        
        for name in valid_names:
            is_valid, error = ProjectValidator.validate_section_name(name)
            assert is_valid, f"'{name}' should be valid: {error}"
    
    def test_validate_section_name_invalid(self):
        """Test invalid section names."""
        invalid_cases = [
            ("", "Section name cannot be empty"),
            ("a", "Section name must be at least 2 characters long"),
            ("a" * 51, "Section name must be less than 50 characters"),
            ("section name", "can only contain letters, numbers, underscores, and hyphens"),
            ("123section", "Section name must start with a letter"),
            ("-section", "Section name must start with a letter"),
        ]
        
        for name, expected_error in invalid_cases:
            is_valid, error = ProjectValidator.validate_section_name(name)
            assert not is_valid
            assert expected_error in error