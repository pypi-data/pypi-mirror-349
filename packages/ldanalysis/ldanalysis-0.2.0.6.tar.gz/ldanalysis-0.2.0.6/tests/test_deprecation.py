"""Test deprecation handling functionality."""

import pytest
from unittest.mock import Mock
from lda.cli.deprecation import DeprecationHandler
from lda.display.console import Console


class TestDeprecationHandler:
    """Test deprecation warning and version handling."""
    
    def test_should_use_strict_mode_explicit(self):
        """Test explicit strict flag overrides everything."""
        assert DeprecationHandler.should_use_strict_mode(
            explicit_strict=True, 
            legacy_mode=False, 
            version="0.1.0"
        ) is True
        
        assert DeprecationHandler.should_use_strict_mode(
            explicit_strict=True, 
            legacy_mode=True, 
            version="0.1.0"
        ) is True
    
    def test_should_use_strict_mode_legacy(self):
        """Test legacy mode disables strict."""
        assert DeprecationHandler.should_use_strict_mode(
            explicit_strict=False, 
            legacy_mode=True, 
            version="0.5.0"
        ) is False
    
    def test_should_use_strict_mode_version(self):
        """Test version-based strict mode."""
        # Before 0.4.0 - not strict
        assert DeprecationHandler.should_use_strict_mode(
            explicit_strict=False, 
            legacy_mode=False, 
            version="0.3.9"
        ) is False
        
        # At 0.4.0 - strict
        assert DeprecationHandler.should_use_strict_mode(
            explicit_strict=False, 
            legacy_mode=False, 
            version="0.4.0"
        ) is True
        
        # After 0.4.0 - strict
        assert DeprecationHandler.should_use_strict_mode(
            explicit_strict=False, 
            legacy_mode=False, 
            version="0.5.0"
        ) is True
    
    def test_check_legacy_usage_no_warnings(self):
        """Test no warnings for proper usage."""
        display = Console()
        
        args = Mock()
        args.name = "Project Name"
        args.analyst = "john.doe"
        args.strict = False
        
        result = DeprecationHandler.check_legacy_usage(args, display)
        assert result is False
    
    def test_check_legacy_usage_with_warnings(self):
        """Test warnings for legacy usage."""
        display = Console()
        
        args = Mock()
        args.name = None
        args.analyst = None
        args.strict = False
        args.use_defaults = True
        
        result = DeprecationHandler.check_legacy_usage(args, display)
        assert result is True
    
    def test_migration_guide_content(self):
        """Test migration guide contains key information."""
        guide = DeprecationHandler.get_migration_guide()
        
        assert "Migration Guide" in guide
        assert "--name" in guide
        assert "--analyst" in guide
        assert "lda profile setup" in guide
        assert "CI/CD" in guide
        assert "v0.4.0" in guide