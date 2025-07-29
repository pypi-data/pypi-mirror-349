"""Validation rules and error messages for LDA."""

import re
from typing import Tuple, List


class ProjectValidator:
    """Validates project initialization parameters."""
    
    # Reserved words that cannot be used as project names
    RESERVED_WORDS = {
        'lda', 'test', 'tests', 'docs', 'dist', 'build', 'src',
        'lib', 'bin', 'tmp', 'temp', 'cache', 'config', 'configs'
    }
    
    # System paths that should not be used
    RESERVED_PATHS = {
        '.', '..', '/', '\\', '~', '$HOME', '$PWD'
    }
    
    @classmethod
    def validate_project_name(cls, name: str) -> Tuple[bool, str]:
        """Validate project name."""
        if not name or not name.strip():
            return False, "Project name cannot be empty"
        
        name = name.strip()
        
        # Check length
        if len(name) < 3:
            return False, "Project name must be at least 3 characters long"
        
        if len(name) > 100:
            return False, "Project name must be less than 100 characters"
        
        # Check for reserved words
        if name.lower() in cls.RESERVED_WORDS:
            return False, f"'{name}' is a reserved word and cannot be used as a project name"
        
        # Check for system paths
        if name in cls.RESERVED_PATHS:
            return False, f"'{name}' is a system path and cannot be used as a project name"
        
        # Check for valid characters (letters, numbers, spaces, underscores, hyphens)
        if not re.match(r'^[a-zA-Z0-9\s_-]+$', name):
            return False, "Project name can only contain letters, numbers, spaces, underscores, and hyphens"
        
        # Check that it starts with a letter or number
        if not re.match(r'^[a-zA-Z0-9]', name):
            return False, "Project name must start with a letter or number"
        
        return True, ""
    
    @classmethod
    def validate_analyst_name(cls, name: str) -> Tuple[bool, str]:
        """Validate analyst name."""
        if not name or not name.strip():
            return False, "Analyst name cannot be empty"
        
        name = name.strip()
        
        # Check length
        if len(name) < 2:
            return False, "Analyst name must be at least 2 characters long"
        
        if len(name) > 50:
            return False, "Analyst name must be less than 50 characters"
        
        # Allow letters, numbers, dots, underscores, hyphens, and spaces
        if not re.match(r'^[a-zA-Z0-9._\s-]+$', name):
            return False, "Analyst name can only contain letters, numbers, dots, underscores, hyphens, and spaces"
        
        # Must start with a letter
        if not re.match(r'^[a-zA-Z]', name):
            return False, "Analyst name must start with a letter"
        
        return True, ""
    
    @classmethod
    def validate_project_code(cls, code: str) -> Tuple[bool, str]:
        """Validate project code."""
        if not code or not code.strip():
            return False, "Project code cannot be empty"
        
        code = code.strip()
        
        # Check length
        if len(code) < 2:
            return False, "Project code must be at least 2 characters long"
        
        if len(code) > 20:
            return False, "Project code must be less than 20 characters"
        
        # Only allow alphanumeric and underscore
        if not re.match(r'^[a-zA-Z0-9_]+$', code):
            return False, "Project code can only contain letters, numbers, and underscores"
        
        # Must start with a letter
        if not re.match(r'^[a-zA-Z]', code):
            return False, "Project code must start with a letter"
        
        # Check for reserved words
        if code.lower() in cls.RESERVED_WORDS:
            return False, f"'{code}' is a reserved word and cannot be used as a project code"
        
        return True, ""
    
    @classmethod
    def validate_email(cls, email: str) -> Tuple[bool, str]:
        """Validate email address."""
        if not email:
            return True, ""  # Email is optional
        
        email = email.strip()
        
        # Basic email validation regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        return True, ""
    
    @classmethod
    def validate_section_name(cls, name: str) -> Tuple[bool, str]:
        """Validate section name."""
        if not name or not name.strip():
            return False, "Section name cannot be empty"
        
        name = name.strip()
        
        # Check length
        if len(name) < 2:
            return False, "Section name must be at least 2 characters long"
        
        if len(name) > 50:
            return False, "Section name must be less than 50 characters"
        
        # Only allow alphanumeric, underscore, and hyphen
        if not re.match(r'^[a-zA-Z0-9_-]+$', name):
            return False, "Section name can only contain letters, numbers, underscores, and hyphens"
        
        # Must start with a letter
        if not re.match(r'^[a-zA-Z]', name):
            return False, "Section name must start with a letter"
        
        return True, ""
    
    @classmethod
    def get_required_fields(cls) -> dict:
        """Get required fields configuration."""
        return {
            'name': {
                'required': True,
                'validator': cls.validate_project_name,
                'error_template': "Project name is required for initialization.\n\n"
                                "Example: lda init --name 'Climate Study 2024' --analyst 'jane.doe'"
            },
            'analyst': {
                'required': True,
                'validator': cls.validate_analyst_name,
                'error_template': "Analyst name is required for provenance tracking.\n\n"
                                "Example: lda init --name 'Climate Study 2024' --analyst 'jane.doe'"
            }
        }
    
    @classmethod
    def format_validation_error(cls, field: str, error: str, value: str = None) -> str:
        """Format a validation error message."""
        lines = [
            f"Validation Error: {field}",
            "-" * 40,
            error
        ]
        
        if value:
            lines.append(f"\nProvided value: '{value}'")
        
        # Add field-specific help
        if field == 'name':
            lines.extend([
                "\nProject names must:",
                "- Be 3-100 characters long",
                "- Start with a letter or number",
                "- Contain only letters, numbers, spaces, underscores, and hyphens",
                "- Not use reserved words (test, docs, config, etc.)"
            ])
        elif field == 'analyst':
            lines.extend([
                "\nAnalyst names must:",
                "- Be 2-50 characters long",
                "- Start with a letter",
                "- Contain only letters, numbers, dots, underscores, hyphens, and spaces"
            ])
        elif field == 'code':
            lines.extend([
                "\nProject codes must:",
                "- Be 2-20 characters long",
                "- Start with a letter",
                "- Contain only letters, numbers, and underscores",
                "- Not use reserved words"
            ])
        
        return "\n".join(lines)