"""
Core functionality for LDA package
"""

from .scaffold import LDAScaffold
from .manifest import LDAManifest
from .tracking import FileTracker
from .errors import LDAError, MissingPlaceholderError
from .profile import UserProfile
from .name_parser import ProjectNameParser
from .validation import ProjectValidator

__all__ = [
    "LDAScaffold",
    "LDAManifest", 
    "FileTracker",
    "LDAError",
    "MissingPlaceholderError",
    "UserProfile",
    "ProjectNameParser",
    "ProjectValidator"
]