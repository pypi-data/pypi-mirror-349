"""User profile management for LDA."""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional


class UserProfile:
    """Manages user-specific defaults and preferences."""
    
    def __init__(self, profile_path: Optional[str] = None):
        """Initialize user profile manager."""
        if profile_path:
            self.profile_path = Path(profile_path)
        else:
            self.profile_path = self._get_default_profile_path()
        
        self.profile = self._load_profile()
    
    def _get_default_profile_path(self) -> Path:
        """Get default profile path based on OS."""
        if os.name == 'nt':  # Windows
            base = Path(os.environ.get('APPDATA', '~'))
        else:  # Unix-like
            base = Path(os.environ.get('XDG_CONFIG_HOME', '~/.config'))
        
        return base.expanduser() / 'lda' / 'profile.yaml'
    
    def _load_profile(self) -> Dict[str, Any]:
        """Load profile from disk or return defaults."""
        if self.profile_path.exists():
            try:
                with open(self.profile_path, 'r') as f:
                    return yaml.safe_load(f) or {}
            except Exception:
                # If profile is corrupted, return empty dict
                return {}
        return {}
    
    def save(self) -> None:
        """Save profile to disk."""
        self.profile_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.profile_path, 'w') as f:
            yaml.dump(self.profile, f, default_flow_style=False)
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get value from profile with dot notation support."""
        keys = key.split('.')
        value = self.profile
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def set(self, key: str, value: Any) -> None:
        """Set value in profile with dot notation support."""
        keys = key.split('.')
        config = self.profile
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
        self.save()
    
    def get_defaults(self) -> Dict[str, Any]:
        """Get all default values for project initialization."""
        return {
            'analyst': self.get('defaults.analyst'),
            'organization': self.get('defaults.organization'),
            'email': self.get('defaults.email'),
            'language': self.get('defaults.language', 'python')
        }
    
    def setup_interactive(self) -> None:
        """Interactive setup for first-time users."""
        print("LDA Profile Setup")
        print("-" * 40)
        print("This will set up default values for your projects.")
        print("You can change these anytime by editing: " + str(self.profile_path))
        print()
        
        # Get analyst name
        analyst = input("Your name (for provenance tracking): ").strip()
        if analyst:
            self.set('defaults.analyst', analyst)
        
        # Get organization
        org = input("Organization (optional): ").strip()
        if org:
            self.set('defaults.organization', org)
        
        # Get email
        email = input("Email (optional): ").strip()
        if email:
            self.set('defaults.email', email)
        
        # Get default language
        lang = input("Default language [python/r/both] (default: python): ").strip().lower()
        if lang in ['python', 'r', 'both']:
            self.set('defaults.language', lang)
        
        print()
        print("Profile saved to:", self.profile_path)
        print("You can edit this file anytime to update your defaults.")