"""Deprecation handling for LDA CLI."""

import warnings
from functools import wraps
from typing import Callable
from ..display.console import Console


class DeprecationHandler:
    """Manages deprecation warnings and migration paths."""
    
    # Version where behavior changes
    STRICT_DEFAULT_VERSION = "0.2.0"
    REMOVAL_VERSION = "0.3.0"
    
    @classmethod
    def show_init_deprecation_warning(cls, display: Console, current_version: str) -> None:
        """Show deprecation warning for init command."""
        display.warning(
            f"Notice: As of v{cls.STRICT_DEFAULT_VERSION}, strict mode is now the default.\n"
            "Required fields (name, analyst) must be provided.\n"
            f"Legacy behavior will be removed in v{cls.REMOVAL_VERSION}.\n\n"
            "To use legacy behavior temporarily:\n"
            "- Use --legacy flag to disable strict validation\n"
            "- Better: Set up a user profile: lda profile setup\n"
            "- Best: Always provide --name and --analyst flags"
        )
    
    @classmethod
    def should_use_strict_mode(cls, explicit_strict: bool, legacy_mode: bool, version: str) -> bool:
        """Determine if strict mode should be used based on version and flags."""
        if explicit_strict:
            return True
        
        if legacy_mode:
            return False
        
        # Check version to determine default behavior
        from packaging import version as pkg_version
        current = pkg_version.parse(version)
        strict_default = pkg_version.parse(cls.STRICT_DEFAULT_VERSION)
        
        return current >= strict_default
    
    @classmethod
    def check_legacy_usage(cls, args, display: Console) -> bool:
        """Check if user is using legacy patterns and warn them."""
        legacy_patterns = []
        
        # Check for missing required fields
        if not args.name:
            legacy_patterns.append("Missing project name")
        
        if not args.analyst:
            legacy_patterns.append("Missing analyst name")
        
        # Check for using defaults that will be removed
        if hasattr(args, 'use_defaults') and args.use_defaults:
            legacy_patterns.append("Using automatic defaults")
        
        if legacy_patterns and not args.strict:
            display.warning(
                "Legacy Usage Detected:\n" +
                "\n".join(f"  - {pattern}" for pattern in legacy_patterns) +
                "\n\nThese patterns will not work in future versions.\n"
                "Use --strict flag to test the new behavior."
            )
            return True
        
        return False
    
    @classmethod
    def wrap_deprecated_function(cls, func: Callable, message: str) -> Callable:
        """Decorator for deprecated functions."""
        @wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(message, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)
        return wrapper
    
    @classmethod
    def get_migration_guide(cls) -> str:
        """Get migration guide for users."""
        return """
Migration Guide: Transitioning from Legacy Mode
==============================================

As of v0.2.0, LDA requires explicit values for project initialization by default.
Legacy mode is deprecated and will be removed in v0.3.0.

Required Changes:
1. Always provide --name and --analyst flags when initializing projects
2. Set up a user profile for default values: lda profile setup
3. Update scripts to provide required values explicitly

Example Migration:

Old (deprecated):
  lda init
  lda init --legacy

Current (required):
  lda init --name "Climate Study 2024" --analyst "jane.doe"

Setting Up Defaults:
  lda profile setup
  
This will create ~/.config/lda/profile.yaml with your default values.

For CI/CD Environments:
  export LDA_ANALYST="ci-bot"
  export LDA_ORGANIZATION="AutomatedTests"
  lda init --name "$PROJECT_NAME"
"""