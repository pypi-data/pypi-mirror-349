"""Main CLI entry point for LDA package."""

import sys
import argparse
from pathlib import Path
from typing import Optional, List

from .commands import Commands
from .utils import find_project_root, setup_logging
from .docs_command import docs_group
from ..config import LDAConfig
from ..display.console import Console
from .. import __version__


class LDACLI:
    """Main CLI interface for LDA."""
    
    def __init__(self):
        """Initialize CLI."""
        self.commands = Commands()
        self.display = Console()
        self.parser = self._create_parser()
    
    def _create_parser(self) -> argparse.ArgumentParser:
        """Create argument parser."""
        parser = argparse.ArgumentParser(
            prog="lda",
            description="Linked Document Analysis - Project management and provenance tracking",
            formatter_class=argparse.RawDescriptionHelpFormatter
        )
        
        # Global options
        parser.add_argument(
            "--version",
            action="version",
            version=f"LDAnalysis v{__version__}"
        )
        
        parser.add_argument(
            "--config", "-c",
            help="Path to configuration file",
            type=str
        )
        
        parser.add_argument(
            "--verbose", "-v",
            help="Enable verbose output",
            action="store_true"
        )
        
        parser.add_argument(
            "--quiet", "-q",
            help="Suppress non-error output",
            action="store_true"
        )
        
        # Create subparsers for commands
        subparsers = parser.add_subparsers(
            dest="command",
            help="Available commands"
        )
        
        # Init command
        init_parser = subparsers.add_parser(
            "init",
            help="Initialize new LDA project"
        )
        init_parser.add_argument(
            "--template", "-t",
            help="Project template to use",
            default="default"
        )
        init_parser.add_argument(
            "--name", "-n",
            help="Project name"
        )
        init_parser.add_argument(
            "--analyst", "-a",
            help="Analyst name"
        )
        init_parser.add_argument(
            "--sections", "-s",
            help="Comma-separated list of sections to create",
            type=str
        )
        init_parser.add_argument(
            "--no-playground",
            help="Skip playground directory creation",
            action="store_true"
        )
        init_parser.add_argument(
            "--language", "-l",
            help="Language for run scripts",
            choices=["python", "r", "both"],
            default="python"
        )
        init_parser.add_argument(
            "--strict",
            help="Use strict validation (default as of v0.2.0)",
            action="store_true"
        )
        init_parser.add_argument(
            "--legacy",
            help="Use legacy validation (will be removed in v0.3.0)",
            action="store_true"
        )
        init_parser.add_argument(
            "--structured",
            help="Use structured naming system for project names",
            action="store_true"
        )
        init_parser.add_argument(
            "--naming-template",
            help="Path to naming template YAML file",
            type=str
        )
        init_parser.add_argument(
            "--force-overwrite",
            help="Force overwrite if a project already exists in the target folder",
            action="store_true"
        )
        init_parser.add_argument(
            "--force-existing",
            help="Use existing folder even if it's not empty",
            action="store_true"
        )
        
        # Status command
        status_parser = subparsers.add_parser(
            "status",
            help="Show project status"
        )
        status_parser.add_argument(
            "--format", "-f",
            help="Output format (text, json)",
            choices=["text", "json"],
            default="text"
        )
        
        # Track command
        track_parser = subparsers.add_parser(
            "track",
            help="Track files in manifest"
        )
        track_parser.add_argument(
            "file",
            help="File to track"
        )
        track_parser.add_argument(
            "--section", "-s",
            help="Section name",
            required=True
        )
        track_parser.add_argument(
            "--type", "-t",
            help="File type (input/output)",
            choices=["input", "output"],
            required=True
        )
        
        # Changes command
        changes_parser = subparsers.add_parser(
            "changes",
            help="Show file changes"
        )
        changes_parser.add_argument(
            "--section", "-s",
            help="Filter by section"
        )
        
        # History command
        history_parser = subparsers.add_parser(
            "history",
            help="Show project history"
        )
        history_parser.add_argument(
            "--limit", "-l",
            help="Number of entries to show",
            type=int,
            default=10
        )
        
        # Validate command
        validate_parser = subparsers.add_parser(
            "validate",
            help="Validate project structure"
        )
        validate_parser.add_argument(
            "--fix",
            help="Attempt to fix issues",
            action="store_true"
        )
        
        # Sync command
        sync_parser = subparsers.add_parser(
            "sync",
            help="Sync project structure with configuration"
        )
        sync_parser.add_argument(
            "--config", "-c",
            help="Path to configuration file (if not in current directory)",
            type=str
        )
        sync_parser.add_argument(
            "--dry-run",
            help="Show what would be changed without making changes",
            action="store_true"
        )
        sync_parser.add_argument(
            "--force-overwrite",
            help="Force overwrite if a project already exists in the target folder",
            action="store_true"
        )
        sync_parser.add_argument(
            "--force-existing",
            help="Use existing folder even if it's not empty",
            action="store_true"
        )
        
        # Export command
        export_parser = subparsers.add_parser(
            "export",
            help="Export manifest or reports"
        )
        export_parser.add_argument(
            "type",
            help="Export type",
            choices=["manifest", "report"]
        )
        export_parser.add_argument(
            "--output", "-o",
            help="Output file",
            required=True
        )
        export_parser.add_argument(
            "--format", "-f",
            help="Output format",
            choices=["csv", "json", "html"],
            default="csv"
        )
        
        # Docs command
        docs_parser = subparsers.add_parser(
            "docs",
            help="Documentation commands"
        )
        
        docs_subparsers = docs_parser.add_subparsers(
            dest="docs_command",
            help="Documentation subcommands"
        )
        
        # Docs serve
        serve_parser = docs_subparsers.add_parser(
            "serve",
            help="Serve documentation locally"
        )
        serve_parser.add_argument(
            "--port", "-p",
            help="Port to serve on",
            type=int,
            default=8000
        )
        serve_parser.add_argument(
            "--dev", "-d",
            help="Enable development mode",
            action="store_true"
        )
        
        # Docs build
        build_parser = docs_subparsers.add_parser(
            "build",
            help="Build documentation site"
        )
        build_parser.add_argument(
            "--output", "-o",
            help="Output directory",
            default="site"
        )
        build_parser.add_argument(
            "--strict", "-s",
            help="Enable strict mode",
            action="store_true"
        )
        build_parser.add_argument(
            "--clean", "-c",
            help="Clean build directory first",
            action="store_true"
        )
        
        # Profile command
        profile_parser = subparsers.add_parser(
            "profile",
            help="Manage user profile and defaults"
        )
        
        profile_subparsers = profile_parser.add_subparsers(
            dest="profile_command",
            help="Profile subcommands"
        )
        
        # Profile setup
        profile_setup = profile_subparsers.add_parser(
            "setup",
            help="Interactive profile setup"
        )
        
        # Profile show
        profile_show = profile_subparsers.add_parser(
            "show",
            help="Show current profile"
        )
        
        # Profile set
        profile_set = profile_subparsers.add_parser(
            "set",
            help="Set profile value"
        )
        profile_set.add_argument(
            "key",
            help="Profile key (e.g., defaults.analyst)"
        )
        profile_set.add_argument(
            "value",
            help="Value to set"
        )
        
        return parser
    
    def run(self, args: Optional[List[str]] = None) -> int:
        """Run the CLI."""
        logger = None
        try:
            # Parse arguments
            parsed_args = self.parser.parse_args(args)
            
            # Set up logging
            logger = setup_logging(
                verbose=getattr(parsed_args, 'verbose', False),
                quiet=getattr(parsed_args, 'quiet', False)
            )
            
            # Handle no command
            if not getattr(parsed_args, 'command', None):
                self.parser.print_help()
                return 0
            
            # Load configuration if specified
            config = None
            if getattr(parsed_args, 'config', None):
                config = LDAConfig(parsed_args.config)
            
            # Execute command
            if hasattr(parsed_args, 'command') and parsed_args.command:
                command_func = getattr(self.commands, f"cmd_{parsed_args.command}")
                return command_func(parsed_args, config, self.display)
            else:
                self.parser.print_help()
                return 0
            
        except KeyboardInterrupt:
            self.display.error("Operation cancelled by user")
            return 130
        
        except Exception as e:
            self.display.error(str(e))
            
            if getattr(parsed_args, 'verbose', False):
                import traceback
                traceback.print_exc()
            
            return 1
        
        finally:
            # Clean up empty log files
            if logger:
                logger.cleanup()


def main():
    """Main entry point for CLI."""
    cli = LDACLI()
    sys.exit(cli.run())