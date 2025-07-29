"""Test interactive CLI functionality."""

import pytest
from unittest.mock import Mock, patch
from lda.cli.interactive import InteractivePrompt
from lda.display.console import Console


class TestInteractivePrompt:
    """Test interactive prompting functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.display = Console()
        self.prompt = InteractivePrompt(self.display)
    
    def test_non_tty_auto_confirm(self):
        """Test that non-TTY environments auto-confirm."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = False
        
        assert prompt.confirm_values({'name': 'test'}) is True
    
    @patch('builtins.input', return_value='y')
    def test_confirm_values_accept(self, mock_input):
        """Test confirming values with 'y'."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        values = {'name': 'Test Project', 'analyst': 'john.doe'}
        assert prompt.confirm_values(values) is True
    
    @patch('builtins.input', return_value='n')
    def test_confirm_values_reject(self, mock_input):
        """Test rejecting values with 'n'."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        values = {'name': 'Test Project', 'analyst': 'john.doe'}
        assert prompt.confirm_values(values) is False
    
    @patch('builtins.input', return_value='test.user')
    def test_prompt_required_field(self, mock_input):
        """Test prompting for required field."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        result = prompt.prompt_required_field("analyst")
        assert result == "test.user"
    
    @patch('builtins.input', return_value='')
    def test_prompt_required_field_with_suggestion(self, mock_input):
        """Test prompting with suggestion."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        result = prompt.prompt_required_field("analyst", suggestion="john.doe")
        assert result == "john.doe"
    
    @patch('builtins.input', side_effect=['invalid@name', 'valid.name'])
    def test_prompt_with_validator(self, mock_input):
        """Test prompting with validation."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        def validator(value):
            if '@' in value:
                return False, "Invalid character '@'"
            return True, ""
        
        result = prompt.prompt_required_field("analyst", validator=validator)
        assert result == "valid.name"
        assert mock_input.call_count == 2
    
    @patch('builtins.input', return_value='optional@example.com')
    def test_prompt_optional_field(self, mock_input):
        """Test prompting for optional field."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        result = prompt.prompt_optional_field("email")
        assert result == "optional@example.com"
    
    @patch('builtins.input', return_value='')
    def test_prompt_optional_field_default(self, mock_input):
        """Test optional field with default."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        result = prompt.prompt_optional_field("language", default="python")
        assert result == "python"
    
    @patch('builtins.input', return_value='2')
    def test_select_option(self, mock_input):
        """Test option selection."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        options = ["Option 1", "Option 2", "Option 3"]
        result = prompt.select_option("Choose one:", options)
        assert result == 1
    
    @patch('builtins.input', return_value='')
    def test_select_option_default(self, mock_input):
        """Test option selection with default."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        options = ["Option 1", "Option 2", "Option 3"]
        result = prompt.select_option("Choose one:", options, default=2)
        assert result == 2
    
    def test_show_extracted_values(self, capsys):
        """Test showing extracted values."""
        prompt = InteractivePrompt(self.display)
        
        extracted = {
            'analyst': 'smith',
            'code': 'ALS301',
            'date': '2024'
        }
        
        prompt.show_extracted_values(extracted, confidence=0.8)
        
        captured = capsys.readouterr()
        assert "Detected Values" in captured.out
        assert "Analyst: smith" in captured.out
        assert "Code: ALS301" in captured.out
        assert "Confidence: 80%" in captured.out
    
    @patch('builtins.input', side_effect=['john.doe'])
    def test_prompt_missing_required(self, mock_input):
        """Test prompting for missing required fields."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        required_fields = {
            'name': {'required': True},
            'analyst': {'required': True}
        }
        
        provided = {'name': 'Test Project'}
        suggestions = {'analyst': 'suggested.user'}
        
        result = prompt.prompt_missing_required(required_fields, provided, suggestions)
        
        assert result['name'] == 'Test Project'
        assert result['analyst'] == 'john.doe'
    
    @patch('builtins.input', return_value='y')
    def test_setup_profile_prompt(self, mock_input):
        """Test profile setup prompt."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        assert prompt.setup_profile_prompt() is True
    
    @patch('builtins.input', return_value='n')
    def test_setup_profile_prompt_decline(self, mock_input):
        """Test declining profile setup."""
        prompt = InteractivePrompt(self.display)
        prompt.is_tty = True
        
        assert prompt.setup_profile_prompt() is False