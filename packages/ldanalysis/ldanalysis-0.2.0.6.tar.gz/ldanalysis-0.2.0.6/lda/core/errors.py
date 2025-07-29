"""Custom error classes for LDA package."""


class LDAError(Exception):
    """Base class for LDA-specific errors."""
    pass


class MissingPlaceholderError(LDAError):
    """Raised when a placeholder is missing from the configuration."""
    
    def __init__(self, missing: list, pattern: str, section: str = None):
        self.missing = missing
        self.pattern = pattern
        self.section = section
        msg = f"Missing placeholder values: {', '.join(missing)} in pattern: {pattern}"
        if section:
            msg += f" (section: {section})"
        super().__init__(msg)


class ConfigurationError(LDAError):
    """Raised when there's an error in the configuration."""
    pass


class ManifestError(LDAError):
    """Raised when there's an error with the manifest."""
    pass


class ScaffoldError(LDAError):
    """Raised when there's an error during scaffold generation."""
    pass


class FileTrackingError(LDAError):
    """Raised when there's an error with file tracking."""
    pass


class CLIError(LDAError):
    """Raised when there's an error in the CLI."""
    pass


class TrackingError(LDAError):
    """Raised when there's an error with tracking."""
    pass


class FolderExistsError(LDAError):
    """Raised when attempting to create a project in a folder that already exists."""
    
    def __init__(self, folder_path: str, has_manifest: bool = False):
        self.folder_path = folder_path
        self.has_manifest = has_manifest
        
        if has_manifest:
            msg = f"Cannot create project: folder '{folder_path}' already contains an LDA project"
        else:
            msg = f"Cannot create project: folder '{folder_path}' already exists"
        
        super().__init__(msg)