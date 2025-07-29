"""CLI command implementations for LDA package."""

import os
import json
from pathlib import Path
from typing import Optional

from ..config import LDAConfig
from ..core.scaffold import LDAScaffold
from ..core.manifest import LDAManifest
from ..core.profile import UserProfile
from ..core.name_parser import ProjectNameParser
from ..core.validation import ProjectValidator
from ..core.name_builder import NameBuilder, NameTemplate
from ..core.errors import FolderExistsError
from ..display.console import Console
from .utils import find_project_root
from .commands_docs import DocsCommands
from .interactive import InteractivePrompt
from .deprecation import DeprecationHandler


class Commands:
    """CLI command implementations."""
    
    @staticmethod
    def cmd_init(args, config: Optional[LDAConfig], display: Console) -> int:
        """Initialize new LDA project with strict validation and smart defaults."""
        display.header("LDA Project Initialization")
        
        # Check for force flags
        force_overwrite = hasattr(args, 'force_overwrite') and args.force_overwrite
        force_existing = hasattr(args, 'force_existing') and args.force_existing
        
        # Initialize components
        interactive = InteractivePrompt(display)
        profile = UserProfile()
        
        # Check for version info (would come from package)
        current_version = "0.2.0.1"  # Should be from __version__
        
        # Determine if we should use strict mode
        strict_mode = DeprecationHandler.should_use_strict_mode(
            args.strict, 
            hasattr(args, 'legacy') and args.legacy, 
            current_version
        )
        
        # Show deprecation warning if using legacy mode
        if args.legacy:
            DeprecationHandler.show_init_deprecation_warning(display, current_version)
        
        # Check if user profile exists, offer to create if not
        if not profile.profile and interactive.is_tty:
            if interactive.setup_profile_prompt():
                profile.setup_interactive()
                print()  # Add spacing after profile setup
        
        # Get values from different sources
        provided_values = {
            'name': args.name,
            'analyst': args.analyst
        }
        
        # Check if user wants structured naming
        use_structured_naming = args.structured if hasattr(args, 'structured') else False
        if not args.name and interactive.is_tty and not use_structured_naming:
            # Ask if they want to use structured naming
            display.info("Would you like to use the structured naming system to build your project name?")
            response = input("Use structured naming? [Y/n]: ").strip().lower()
            use_structured_naming = response != 'n'
        
        # Use structured naming if requested
        if use_structured_naming and interactive.is_tty:
            # Load template if specified
            template = None
            if hasattr(args, 'naming_template') and args.naming_template:
                try:
                    template_path = Path(args.naming_template)
                    template = NameTemplate.load_from_file(template_path)
                    display.info(f"Using naming template: {template.name}")
                except Exception as e:
                    display.error(f"Failed to load naming template: {e}")
                    display.info("Using default naming template")
                    template = NameTemplate.get_default()
            else:
                template = NameTemplate.get_default()
            
            # Build project name interactively
            builder = template.get_builder(display)
            project_name = builder.build_interactive()
            args.name = project_name
            display.success(f"Project name created: {project_name}")
        
        # Smart extraction from project name
        suggestions = {}
        if args.name:
            suggestions, confidence = ProjectNameParser.suggest_values(args.name)
            if confidence > 0.5 and interactive.is_tty:
                interactive.show_extracted_values(suggestions, confidence)
        
        # Get profile defaults
        profile_defaults = profile.get_defaults()
        
        # Environment variable overrides
        env_values = {
            'analyst': os.environ.get('LDA_ANALYST'),
            'organization': os.environ.get('LDA_ORGANIZATION'),
            'email': os.environ.get('LDA_EMAIL')
        }
        
        # Priority: CLI args > env vars > profile > suggestions
        final_values = {}
        
        # Merge values with priority
        for field in ['name', 'analyst', 'code', 'organization', 'email']:
            if provided_values.get(field):
                final_values[field] = provided_values[field]
            elif env_values.get(field):
                final_values[field] = env_values[field]
            elif profile_defaults.get(field):
                final_values[field] = profile_defaults[field]
            elif suggestions.get(field):
                # Don't use suggested code if we used structured naming
                if field == 'code' and use_structured_naming:
                    continue
                final_values[field] = suggestions[field]
        
        # In strict mode, enforce required fields
        if strict_mode:
            required_fields = ProjectValidator.get_required_fields()
            
            # Interactive prompting for missing required fields
            if interactive.is_tty:
                final_values = interactive.prompt_missing_required(
                    required_fields,
                    final_values,
                    suggestions
                )
                
                if final_values is None:
                    display.error("Project initialization cancelled")
                    return 1
            else:
                # Non-interactive mode - check for missing required fields
                missing = []
                for field, config in required_fields.items():
                    if field not in final_values or not final_values[field]:
                        missing.append(field)
                
                if missing:
                    for field in missing:
                        error_msg = required_fields[field]['error_template']
                        display.error(f"Missing required field: {field}\n\n{error_msg}")
                    
                    display.info("\nUse --help for more information or set up a profile:")
                    display.info("  lda profile setup")
                    return 1
        
        # Validate all provided values
        errors = []
        
        # Validate project name
        if 'name' in final_values and final_values['name']:
            is_valid, error = ProjectValidator.validate_project_name(final_values['name'])
            if not is_valid:
                errors.append(('name', error, final_values['name']))
        
        # Validate analyst name
        if 'analyst' in final_values and final_values['analyst']:
            is_valid, error = ProjectValidator.validate_analyst_name(final_values['analyst'])
            if not is_valid:
                errors.append(('analyst', error, final_values['analyst']))
        
        # Validate email if provided
        if 'email' in final_values and final_values['email']:
            is_valid, error = ProjectValidator.validate_email(final_values['email'])
            if not is_valid:
                errors.append(('email', error, final_values['email']))
        
        # Show validation errors
        if errors:
            for field, error, value in errors:
                error_msg = ProjectValidator.format_validation_error(field, error, value)
                display.error(error_msg)
            return 1
        
        # Generate project code if not provided
        if 'code' not in final_values or not final_values['code']:
            if final_values.get('name'):
                # Use the full project name as the code for intuitive folder names
                final_values['code'] = final_values['name']
            else:
                final_values['code'] = 'PROJ'
        
        # Sanitize project code for filesystem - preserve original structure
        import re
        # Keep underscores and hyphens, just remove truly problematic characters
        project_code = re.sub(r'[<>:"/\\|?*]', '', final_values['code'])
        # Replace spaces with underscores
        project_code = re.sub(r'\s+', '_', project_code)
        final_values['code'] = project_code
        
        # Interactive confirmation
        if interactive.is_tty and strict_mode:
            if not interactive.confirm_values(final_values, suggestions):
                display.error("Project initialization cancelled")
                return 1
        
        # Don't create the config file yet - we'll save it inside the project folder later
        if not config:
            config = LDAConfig()
        
        # Update config with final values
        for key, value in final_values.items():
            if value is not None:
                config.set(f"project.{key}", value)
        
        # Add force flags to config if provided
        if force_overwrite:
            config.set("force_overwrite", True)
        if force_existing:
            config.set("force_existing", True)
            
        # Handle sections
        sections = []
        if args.sections:
            section_names = [s.strip() for s in args.sections.split(',')]
            for section_name in section_names:
                # Validate section names
                is_valid, error = ProjectValidator.validate_section_name(section_name)
                if not is_valid:
                    display.error(f"Invalid section name '{section_name}': {error}")
                    return 1
                
                sections.append({
                    "name": section_name,
                    "inputs": [],
                    "outputs": []
                })
            config.set("sections", sections)
        elif not config.get("sections"):
            config.set("sections", [])
        
        # Set other options
        config.set("project.create_playground", not args.no_playground)
        config.set("project.language", args.language)
        # Don't set root_folder - we want the subfolder to be created
        
        # Don't save the configuration file yet - wait until we create the project folder
        # We'll save inside the project folder instead
        
        # Create project
        try:
            # Check for force flags
            force_overwrite = hasattr(args, 'force_overwrite') and args.force_overwrite
            force_existing = hasattr(args, 'force_existing') and args.force_existing
            
            # Pass force flags to scaffold
            scaffold = LDAScaffold(config, 
                                force_overwrite=force_overwrite, 
                                force_existing=force_existing)
            result = scaffold.create_project()
            
            display.success(f"Project created at: {result['project_folder']}")
            display.info(f"Sections created: {result['sections']}")
            if not args.no_playground:
                display.info("Playground created: lda_playground/")
            display.info(f"Files created: {len(result['files'])}")
            # Display success message with the correct path to config file
            config_path = Path(result['project_folder']) / "lda_config.yaml"
            display.success(f"Configuration saved: {config_path}")
            display.info(f"Time taken: {result['duration']:.2f}s")
            
            # Show next steps
            display.section("Next Steps")
            
            # By default, we should now always be creating a subfolder
            project_folder_name = os.path.basename(result['project_folder'])
            next_steps = [
                f"cd {project_folder_name}",
                "lda status  # Check project status",
                "lda track <file> --section name --type input  # Track input files"
            ]
            
            display.list_items(next_steps)
            
            return 0
        except FolderExistsError as e:
            # Handle folder exists error with more informative messages
            if e.has_manifest:
                display.error(f"Cannot create project: '{e.folder_path}' already contains an LDA project")
                display.info("Options:")
                display.info("  1. Choose a different project name")
                display.info("  2. Use --force-overwrite to override the existing project (use with caution)")
            else:
                display.error(f"Cannot create project: '{e.folder_path}' already exists but is not an LDA project")
                display.info("Options:")
                display.info("  1. Choose a different project name")
                display.info("  2. Remove or rename the existing folder")
                display.info("  3. Use --force-existing to use the existing folder anyway")
            return 1
            
        except Exception as e:
            display.error(f"Failed to create project: {e}")
            return 1
    
    @staticmethod
    def cmd_status(args, config: Optional[LDAConfig], display: Console) -> int:
        """Show project status."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found in current directory")
            return 1
        
        try:
            manifest = LDAManifest(project_root)
            status = manifest.get_project_status()
            
            # Try to load config if not provided, to get complete project metadata
            if not config:
                # Look for config file in the project folder
                config_file = Path(project_root) / "lda_config.yaml"
                
                # If not found, check the .lda directory
                if not config_file.exists():
                    config_file = Path(project_root) / ".lda" / "config.yaml"
                
                # Legacy fallback - look in parent directory
                if not config_file.exists():
                    parent_dir = Path(project_root).parent
                    project_code = Path(project_root).name
                    config_file = parent_dir / f"{project_code}_config.yaml"
                    
                    if not config_file.exists():
                        # Try legacy filename pattern in parent directory
                        config_file = parent_dir / "lda_config.yaml"
                
                if config_file.exists():
                    config = LDAConfig(str(config_file))
            
            # Merge config data into status if available
            if config:
                if "name" not in status['project'] or status['project']['name'] == 'Unknown':
                    status['project']['name'] = config.get("project.name", "Unknown")
                if "code" not in status['project'] or status['project']['code'] == 'Unknown':
                    status['project']['code'] = config.get("project.code", "Unknown")
                if "analyst" not in status['project'] or status['project']['analyst'] == 'Unknown':
                    status['project']['analyst'] = config.get("project.analyst", "Unknown")
            
            if args.format == "json":
                print(json.dumps(status, indent=2))
            else:
                display.header("Project Status")
                
                # Project info
                display.section("Project Information")
                display.list_items([
                    f"Name: {status['project'].get('name', 'Unknown')}",
                    f"Code: {status['project'].get('code', 'Unknown')}",
                    f"Analyst: {status['project'].get('analyst', 'Unknown')}",
                    f"Created: {status['project'].get('created', 'Unknown')}",
                    f"Root: {status['project'].get('root', 'Unknown')}"
                ])
                
                # Summary
                display.section("Summary")
                display.list_items([
                    f"Sections: {status['sections']}",
                    f"Total files: {status['files']['total']}",
                    f"Input files: {status['files']['inputs']}",
                    f"Output files: {status['files']['outputs']}",
                    f"Last activity: {status.get('last_activity', 'Never')}"
                ])
                
                # Sections detail
                display.section("Sections")
                for section_name, section_info in manifest.manifest["sections"].items():
                    display.list_items([
                        f"{section_name}:",
                        f"  Folder: {section_info['folder']}",
                        f"  Created: {section_info['created']}",
                        f"  Provenance: {section_info['provenance_id']}"
                    ])
            
            return 0
            
        except Exception as e:
            display.error(f"Failed to get status: {e}")
            return 1
    
    @staticmethod
    def cmd_track(args, config: Optional[LDAConfig], display: Console) -> int:
        """Track files in manifest."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found")
            return 1
        
        try:
            manifest = LDAManifest(project_root)
            
            # Track file
            manifest.track_file(
                section=args.section,
                file_type=args.type,
                filename=os.path.basename(args.file)
            )
            
            display.success(f"Tracked {args.type} file: {args.file}")
            return 0
            
        except Exception as e:
            display.error(f"Failed to track file: {e}")
            return 1
    
    @staticmethod
    def cmd_changes(args, config: Optional[LDAConfig], display: Console) -> int:
        """Show file changes."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found")
            return 1
        
        try:
            manifest = LDAManifest(project_root)
            changes = manifest.detect_changes(section=args.section)
            
            display.header("File Changes")
            
            if not any(changes.values()):
                display.info("No changes detected")
            else:
                if changes["new"]:
                    display.section("New Files")
                    display.list_items(changes["new"])
                
                if changes["modified"]:
                    display.section("Modified Files")
                    display.list_items(changes["modified"])
                
                if changes["deleted"]:
                    display.section("Deleted Files")
                    display.list_items(changes["deleted"])
            
            return 0
            
        except Exception as e:
            display.error(f"Failed to check changes: {e}")
            return 1
    
    @staticmethod
    def cmd_history(args, config: Optional[LDAConfig], display: Console) -> int:
        """Show project history."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found")
            return 1
        
        try:
            manifest = LDAManifest(project_root)
            history = manifest.get_history(limit=args.limit)
            
            display.header(f"Project History (last {args.limit} entries)")
            
            for entry in reversed(history):
                display.section(entry["timestamp"])
                display.list_items([
                    f"Action: {entry['action']}",
                    f"Details: {json.dumps(entry['details'], indent=2)}"
                ])
            
            return 0
            
        except Exception as e:
            display.error(f"Failed to get history: {e}")
            return 1
    
    @staticmethod
    def cmd_validate(args, config: Optional[LDAConfig], display: Console) -> int:
        """Validate project structure."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found")
            return 1
        
        display.header("Project Validation")
        
        issues = []
        
        try:
            # Check manifest
            manifest = LDAManifest(project_root)
            
            # Check configuration
            if config:
                config.validate()
            
            # Check sections exist
            for section_name, section_info in manifest.manifest["sections"].items():
                section_path = Path(project_root) / section_info["folder"]
                
                if not section_path.exists():
                    issues.append(f"Section folder missing: {section_path}")
                else:
                    # Check subdirectories
                    if not (section_path / "inputs").exists():
                        issues.append(f"Inputs folder missing: {section_path}/inputs")
                    if not (section_path / "outputs").exists():
                        issues.append(f"Outputs folder missing: {section_path}/outputs")
            
            # Check tracked files
            for file_key, file_info in manifest.manifest["files"].items():
                file_path = Path(project_root) / file_info["path"]
                
                if not file_path.exists():
                    issues.append(f"Tracked file missing: {file_path}")
            
            if issues:
                display.section("Issues Found")
                display.list_items(issues)
                
                if args.fix:
                    display.section("Attempting Fixes")
                    
                    for issue in issues:
                        if "folder missing" in issue:
                            # Create missing folders
                            folder_path = issue.split(": ")[1]
                            Path(folder_path).mkdir(parents=True, exist_ok=True)
                            display.success(f"Created: {folder_path}")
                
                return 1
            else:
                display.success("No issues found")
                return 0
            
        except Exception as e:
            display.error(f"Validation failed: {e}")
            return 1
    
    @staticmethod
    def cmd_export(args, config: Optional[LDAConfig], display: Console) -> int:
        """Export manifest or reports."""
        project_root = find_project_root()
        
        if not project_root:
            display.error("No LDA project found")
            return 1
        
        try:
            manifest = LDAManifest(project_root)
            
            if args.type == "manifest":
                if args.format == "csv":
                    manifest.export_to_csv(args.output)
                elif args.format == "json":
                    with open(args.output, 'w') as f:
                        json.dump(manifest.manifest, f, indent=2)
                else:
                    display.error(f"Unsupported format: {args.format}")
                    return 1
            
            elif args.type == "report":
                # Generate report (to be implemented)
                display.error("Report generation not yet implemented")
                return 1
            
            display.success(f"Exported to: {args.output}")
            return 0
            
        except Exception as e:
            display.error(f"Export failed: {e}")
            return 1
    
    @staticmethod
    def cmd_sync(args, config: Optional[LDAConfig], display: Console) -> int:
        """Sync project structure with configuration."""
        display.header("LDA Project Sync")
        
        # Find configuration file
        if args.config:
            config_file = Path(args.config)
        else:
            # Try to find config file in current directory
            config_files = list(Path.cwd().glob("*_config.yaml"))
            
            # Also check for config files in standard locations
            if Path("lda_config.yaml").exists():
                config_files.append(Path("lda_config.yaml"))
                
            # Check for config in .lda directory
            if Path(".lda/config.yaml").exists():
                config_files.append(Path(".lda/config.yaml"))
                
            # Try to find project root and check there
            project_root = find_project_root()
            if project_root:
                proj_config = Path(project_root) / "lda_config.yaml"
                if proj_config.exists():
                    config_files.append(proj_config)
                
                # Check in .lda directory within project root
                proj_hidden_config = Path(project_root) / ".lda" / "config.yaml"
                if proj_hidden_config.exists():
                    config_files.append(proj_hidden_config)
            
            if not config_files:
                # Create empty config file name for later error message
                config_files = [Path("lda_config.yaml")]
            
            if len(config_files) > 1:
                display.error("Multiple config files found. Please specify one with --config")
                for cf in config_files:
                    display.info(f"  - {cf}")
                return 1
            
            config_file = config_files[0]
        
        if not config_file.exists():
            display.error(f"Configuration file not found: {config_file}")
            return 1
        
        try:
            # Load configuration
            config = LDAConfig(str(config_file))
            display.info(f"Loaded configuration from: {config_file}")
            
            # Find or create project
            project_root = Path.cwd()
            project_code = config.get("project.code", "PROJ")
            
            # Project folder should be a subfolder of current directory by default
            if config.get("project.root_folder") == "USE_CURRENT_DIR":
                project_folder = project_root
            else:
                project_folder = project_root / project_code
            
            # Check if manifest exists in the expected location
            manifest_csv = project_folder / "lda_manifest.csv"
            manifest_json = project_folder / ".lda" / "manifest.json"
            
            # If project doesn't exist at all, create it
            if not project_folder.exists():
                display.info("No existing project found. Creating new project structure...")
                from ..core.scaffold import LDAScaffold
                
                # Get force flags
                force_overwrite = getattr(args, 'force_overwrite', False)
                force_existing = getattr(args, 'force_existing', True)  # Default to True for sync
                
                scaffold = LDAScaffold(config, force_overwrite=force_overwrite, force_existing=force_existing)
                result = scaffold.create_project()
                display.success(f"Project created at: {result['project_folder']}")
                return 0
            
            # If folder exists but no manifest, error
            if not manifest_csv.exists() and not manifest_json.exists():
                display.error(f"Project folder exists at {project_folder} but no manifest found")
                display.info("Run 'lda init' to create a new project")
                return 1
            
            # Existing project - sync changes
            from ..core.manifest import LDAManifest
            manifest = LDAManifest(str(project_folder))
            
            # Get current sections from manifest
            existing_sections = set(manifest.manifest["sections"].keys())
            
            # Get desired sections from config
            config_sections = config.get("sections", [])
            desired_sections = {s["name"] for s in config_sections}
            
            # Sections to add
            sections_to_add = desired_sections - existing_sections
            
            # Sections to remove (in dry-run mode only)
            sections_to_remove = existing_sections - desired_sections
            
            if args.dry_run:
                display.section("Dry Run - Changes to be made:")
                
                if sections_to_add:
                    display.info(f"Sections to create: {', '.join(sections_to_add)}")
                
                if sections_to_remove:
                    display.warning(f"Sections that exist but not in config: {', '.join(sections_to_remove)}")
                    display.info("(These would NOT be removed automatically)")
                
                # Check playground
                playground_dir = project_folder / "lda_playground"
                create_playground = config.get("project.create_playground", True)
                
                if create_playground and not playground_dir.exists():
                    display.info("Would create playground directory")
                elif not create_playground and playground_dir.exists():
                    display.warning("Playground exists but not in config (would NOT be removed)")
                
                if not sections_to_add and not (create_playground and not playground_dir.exists()):
                    display.info("No changes needed")
                
                return 0
            
            # Make actual changes
            from ..core.scaffold import LDAScaffold
            
            # Get force flags
            force_overwrite = getattr(args, 'force_overwrite', False)
            force_existing = getattr(args, 'force_existing', True)  # Default to True for sync
            
            scaffold = LDAScaffold(config, force_overwrite=force_overwrite, force_existing=force_existing)
            scaffold.manifest = manifest  # Use existing manifest
            
            changes_made = False
            
            # Add new sections
            for section_name in sections_to_add:
                section_config = next(s for s in config_sections if s["name"] == section_name)
                scaffold.create_section(section_config)
                display.success(f"Created section: {section_name}")
                changes_made = True
            
            # Create playground if needed
            playground_dir = project_folder / "lda_playground"
            if config.get("project.create_playground", True) and not playground_dir.exists():
                scaffold.create_playground()
                display.success("Created playground directory")
                changes_made = True
            
            # Update project files (README, etc.)
            if changes_made:
                scaffold.create_project_files()
                display.success("Updated project files")
            else:
                display.info("No changes needed")
            
            # Show warnings for items not in config
            if sections_to_remove:
                display.warning(f"Sections exist but not in config: {', '.join(sections_to_remove)}")
                display.info("These sections were NOT removed. Remove manually if needed.")
            
            return 0
            
        except Exception as e:
            display.error(f"Sync failed: {e}")
            if hasattr(args, 'verbose') and args.verbose:
                import traceback
                traceback.print_exc()
            return 1
    
    @staticmethod
    def cmd_docs(args, config: Optional[LDAConfig], display: Console) -> int:
        """Documentation commands."""
        docs_commands = DocsCommands()
        
        # Handle subcommands
        if args.docs_command == "serve":
            return docs_commands.serve(
                port=args.port if hasattr(args, 'port') else 8000,
                dev=args.dev if hasattr(args, 'dev') else False
            )
        elif args.docs_command == "build":
            return docs_commands.build(
                output=args.output if hasattr(args, 'output') else 'site',
                strict=args.strict if hasattr(args, 'strict') else False,
                clean=args.clean if hasattr(args, 'clean') else False
            )
        else:
            display.error(f"Unknown docs command: {args.docs_command}")
            return 1
    
    @staticmethod
    def cmd_profile(args, config: Optional[LDAConfig], display: Console) -> int:
        """Profile management commands."""
        profile = UserProfile()
        
        # Handle subcommands
        if args.profile_command == "setup":
            profile.setup_interactive()
            return 0
            
        elif args.profile_command == "show":
            display.header("LDA User Profile")
            
            if not profile.profile:
                display.info("No profile found.")
                display.info("Run 'lda profile setup' to create one.")
                return 0
            
            display.section("Profile Location")
            display.info(str(profile.profile_path))
            
            display.section("Current Settings")
            defaults = profile.get_defaults()
            items = []
            for key, value in defaults.items():
                if value is not None:
                    items.append(f"{key}: {value}")
            
            if items:
                display.list_items(items)
            else:
                display.info("No settings configured")
            
            return 0
            
        elif args.profile_command == "set":
            profile.set(args.key, args.value)
            display.success(f"Set {args.key} = {args.value}")
            return 0
            
        else:
            display.error("Please specify a profile subcommand: setup, show, or set")
            return 1