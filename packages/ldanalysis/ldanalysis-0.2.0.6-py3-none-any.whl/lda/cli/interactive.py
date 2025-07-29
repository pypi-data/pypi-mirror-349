"""Interactive CLI utilities for LDA."""

import sys
from typing import Dict, Any, Optional
from ..display.console import Console


class InteractivePrompt:
    """Handle interactive prompts for missing required fields."""
    
    def __init__(self, display: Console):
        """Initialize interactive prompt handler."""
        self.display = display
        self.is_tty = sys.stdin.isatty() and sys.stdout.isatty()
    
    def confirm_values(self, values: Dict[str, Any], suggestions: Dict[str, Any] = None) -> bool:
        """Confirm extracted or provided values with user."""
        if not self.is_tty:
            return True  # Auto-confirm in non-interactive mode
        
        self.display.section("Project Configuration")
        
        # Display values with suggestions
        items = []
        for key, value in values.items():
            if value is not None:
                # Provide better labels for specific fields
                field_labels = {
                    'name': 'Project Name',
                    'code': 'Folder Name',
                    'analyst': 'Analyst',
                    'organization': 'Organization',
                    'email': 'Email'
                }
                label = field_labels.get(key, key.title())
                
                suggestion = ""
                if suggestions and suggestions.get(key) and suggestions[key] != value:
                    suggestion = f" (detected: {suggestions[key]})"
                items.append(f"{label}: {value}{suggestion}")
        
        self.display.list_items(items)
        
        # Ask for confirmation
        response = input("\nIs this correct? [Y/n]: ").strip().lower()
        return response != 'n'
    
    def prompt_required_field(self, field: str, suggestion: Optional[str] = None, 
                           validator=None) -> Optional[str]:
        """Prompt for a required field with optional suggestion."""
        if not self.is_tty:
            return None
        
        # Provide clearer prompts for specific fields
        field_prompts = {
            'name': "Project name",
            'analyst': "Your name (for provenance tracking)",
            'code': "Project code (folder name)",
            'organization': "Organization",
            'email': "Email"
        }
        
        prompt = field_prompts.get(field, field.title())
        if suggestion:
            prompt += f" [{suggestion}]"
        prompt += ": "
        
        while True:
            value = input(prompt).strip()
            
            # Use suggestion if empty
            if not value and suggestion:
                value = suggestion
            
            # Validate if validator provided
            if value and validator:
                is_valid, error_msg = validator(value)
                if not is_valid:
                    self.display.error(error_msg)
                    continue
            
            return value if value else None
    
    def prompt_optional_field(self, field: str, default: Optional[str] = None) -> Optional[str]:
        """Prompt for an optional field."""
        if not self.is_tty:
            return default
        
        prompt = f"{field.title()}"
        if default:
            prompt += f" [{default}]"
        prompt += " (optional): "
        
        value = input(prompt).strip()
        return value if value else default
    
    def select_option(self, prompt: str, options: list, default: int = 0) -> int:
        """Let user select from a list of options."""
        if not self.is_tty:
            return default
        
        self.display.section(prompt)
        for i, option in enumerate(options):
            marker = ">" if i == default else " "
            print(f"  {marker} {i + 1}. {option}")
        
        while True:
            try:
                choice = input(f"\nSelect option [1-{len(options)}] (default: {default + 1}): ").strip()
                if not choice:
                    return default
                
                idx = int(choice) - 1
                if 0 <= idx < len(options):
                    return idx
                else:
                    self.display.error(f"Please enter a number between 1 and {len(options)}")
            except ValueError:
                self.display.error("Please enter a valid number")
    
    def show_extracted_values(self, extracted: Dict[str, Any], confidence: float) -> None:
        """Show values extracted from project name."""
        if not extracted or not any(extracted.values()):
            return
        
        self.display.section("Detected Values")
        
        items = []
        for key, value in extracted.items():
            if value:
                items.append(f"{key.title()}: {value}")
        
        if items:
            self.display.list_items(items)
            self.display.info(f"Confidence: {confidence:.0%}")
    
    def prompt_missing_required(self, required_fields: Dict[str, Any], 
                              provided: Dict[str, Any],
                              suggestions: Dict[str, Any] = None) -> Dict[str, Any]:
        """Prompt for missing required fields."""
        result = provided.copy()
        
        for field, config in required_fields.items():
            if field not in result or result[field] is None:
                suggestion = suggestions.get(field) if suggestions else None
                validator = config.get('validator')
                
                value = self.prompt_required_field(field, suggestion, validator)
                if value:
                    result[field] = value
                elif config.get('required', True):
                    # If truly required and no value provided, we must fail
                    return None
        
        return result
    
    def setup_profile_prompt(self) -> bool:
        """Ask if user wants to set up a profile."""
        if not self.is_tty:
            return False
        
        self.display.info("No user profile found. A profile can store default values for your projects.")
        response = input("Would you like to set up a profile now? [Y/n]: ").strip().lower()
        return response != 'n'