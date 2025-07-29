"""Test user profile functionality."""

import pytest
import tempfile
import os
from pathlib import Path
from lda.core.profile import UserProfile


class TestUserProfile:
    """Test user profile management."""
    
    def test_profile_creation(self, tmp_path):
        """Test creating a new profile."""
        profile_path = tmp_path / "profile.yaml"
        profile = UserProfile(str(profile_path))
        
        # Initially empty
        assert profile.profile == {}
        assert not profile_path.exists()
    
    def test_profile_save_and_load(self, tmp_path):
        """Test saving and loading profile data."""
        profile_path = tmp_path / "profile.yaml"
        profile = UserProfile(str(profile_path))
        
        # Set some values
        profile.set("defaults.analyst", "john.doe")
        profile.set("defaults.organization", "Research Lab")
        
        # Check file was created
        assert profile_path.exists()
        
        # Load in new instance
        profile2 = UserProfile(str(profile_path))
        assert profile2.get("defaults.analyst") == "john.doe"
        assert profile2.get("defaults.organization") == "Research Lab"
    
    def test_get_with_dot_notation(self, tmp_path):
        """Test getting values with dot notation."""
        profile_path = tmp_path / "profile.yaml"
        profile = UserProfile(str(profile_path))
        
        profile.set("defaults.analyst", "jane.doe")
        profile.set("preferences.color", "blue")
        
        assert profile.get("defaults.analyst") == "jane.doe"
        assert profile.get("preferences.color") == "blue"
        assert profile.get("nonexistent.key") is None
        assert profile.get("nonexistent.key", "default") == "default"
    
    def test_set_with_dot_notation(self, tmp_path):
        """Test setting values with dot notation."""
        profile_path = tmp_path / "profile.yaml"
        profile = UserProfile(str(profile_path))
        
        profile.set("deeply.nested.value", "test")
        
        assert profile.profile["deeply"]["nested"]["value"] == "test"
        assert profile.get("deeply.nested.value") == "test"
    
    def test_get_defaults(self, tmp_path):
        """Test getting default values."""
        profile_path = tmp_path / "profile.yaml"
        profile = UserProfile(str(profile_path))
        
        # Empty profile returns Nones and default language
        defaults = profile.get_defaults()
        assert defaults['analyst'] is None
        assert defaults['organization'] is None
        assert defaults['email'] is None
        assert defaults['language'] == 'python'
        
        # Set some values
        profile.set("defaults.analyst", "test.user")
        profile.set("defaults.email", "test@example.com")
        
        defaults = profile.get_defaults()
        assert defaults['analyst'] == "test.user"
        assert defaults['email'] == "test@example.com"
        assert defaults['language'] == 'python'
    
    def test_default_profile_path(self, monkeypatch):
        """Test default profile path determination."""
        # Mock environment variables
        with tempfile.TemporaryDirectory() as tmpdir:
            # Test Unix-like systems
            monkeypatch.setattr('os.name', 'posix')
            monkeypatch.setenv('XDG_CONFIG_HOME', tmpdir)
            
            profile = UserProfile()
            expected = Path(tmpdir) / 'lda' / 'profile.yaml'
            assert profile.profile_path == expected
            
            # Test Windows
            monkeypatch.setattr('os.name', 'nt')
            monkeypatch.setenv('APPDATA', tmpdir)
            
            profile = UserProfile()
            expected = Path(tmpdir) / 'lda' / 'profile.yaml'
            assert profile.profile_path == expected
    
    def test_corrupted_profile_handling(self, tmp_path):
        """Test handling of corrupted profile files."""
        profile_path = tmp_path / "profile.yaml"
        
        # Write invalid YAML
        profile_path.write_text("invalid: yaml: content:")
        
        # Should return empty dict instead of crashing
        profile = UserProfile(str(profile_path))
        assert profile.profile == {}
    
    def test_profile_persistence(self, tmp_path):
        """Test that profile changes persist."""
        profile_path = tmp_path / "profile.yaml"
        
        # Create and modify profile
        profile1 = UserProfile(str(profile_path))
        profile1.set("test.value", "original")
        
        # Load in new instance
        profile2 = UserProfile(str(profile_path))
        assert profile2.get("test.value") == "original"
        
        # Modify in second instance
        profile2.set("test.value", "modified")
        
        # Check in third instance
        profile3 = UserProfile(str(profile_path))
        assert profile3.get("test.value") == "modified"