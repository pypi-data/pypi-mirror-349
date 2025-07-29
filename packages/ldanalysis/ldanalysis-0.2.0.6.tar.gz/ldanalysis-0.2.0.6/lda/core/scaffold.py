"""Main scaffold generator for LDA projects."""

import os
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any, Optional

from ..config import LDAConfig
from .manifest import LDAManifest
from .tracking import FileTracker
from .template_service import TemplateService
from .errors import ScaffoldError, MissingPlaceholderError


class LDAScaffold:
    """Main scaffold generator for LDA projects."""
    
    def __init__(self, config: LDAConfig, force_overwrite: bool = False, force_existing: bool = False):
        """Initialize with configuration.
    
        Args:
            config: LDAConfig object
            force_overwrite: If True, allow overwriting existing LDA project
            force_existing: If True, allow using an existing directory that isn't an LDA project
        """
        self.config = config
        self.project_root = Path(config.get("project.root_folder", "."))
        self.project_code = config.get("project.code", "PROJ")
        self.template_service = TemplateService()
        
        # Default behavior is to create a subfolder with project code
        # Only if root_folder is explicitly set to "USE_CURRENT_DIR" do we use current directory
        if config.get("project.root_folder") == "USE_CURRENT_DIR":
            self.project_folder = Path.cwd()
        else:
            # Create a subfolder with the project code
            self.project_folder = Path.cwd() / self.project_code

        # Check if folder already exists before creating
        if self.project_folder.exists():
            # Check if it contains an LDA project by looking for manifest files
            manifest_csv = self.project_folder / "lda_manifest.csv"
            manifest_json = self.project_folder / ".lda" / "manifest.json"
            
            if manifest_csv.exists() or (self.project_folder / ".lda").exists() and manifest_json.exists():
                # Folder contains an LDA project
                if not force_overwrite and not config.get("force_overwrite", False):
                    from .errors import FolderExistsError
                    raise FolderExistsError(str(self.project_folder), has_manifest=True)
            else:
                # Folder exists but doesn't have LDA project files
                if not force_existing and not config.get("force_existing", False):
                    from .errors import FolderExistsError
                    raise FolderExistsError(str(self.project_folder), has_manifest=False)
        
        # Create the folder if it passed all safety checks
        self.project_folder.mkdir(parents=True, exist_ok=True)
        
        # Initialize manifest
        self.manifest = LDAManifest(str(self.project_folder))
        self.file_tracker = FileTracker()
        
        # Track created items
        self.created_sections = []
        self.created_files = []
    
    def create_project(self) -> Dict[str, Any]:
        """Create the complete project structure."""
        start_time = datetime.now()
        
        try:
            # Initialize project in manifest
            self.manifest.init_project({
                "name": self.config.get("project.name"),
                "code": self.config.get("project.code"),
                "analyst": self.config.get("project.analyst")
            })
            
            # Create sections
            sections = self.config.get("sections", [])
            for section_config in sections:
                self.create_section(section_config)
            
            # Create playground if enabled
            if self.config.get("project.create_playground", True):
                self.create_playground()
            
            # Create sandbox sections
            sandbox_items = self.config.get("sandbox", [])
            if sandbox_items:
                self.create_sandbox(sandbox_items)
            
            # Create project-level files
            self.create_project_files()
            
            # Save config file inside the project folder
            self.save_project_config()
            
            # Log project creation
            self.manifest.add_history("project_created", {
                "sections": len(self.created_sections),
                "files": len(self.created_files),
                "duration": (datetime.now() - start_time).total_seconds()
            })
            
            return {
                "success": True,
                "project_folder": str(self.project_folder),
                "sections": self.created_sections,
                "files": self.created_files,
                "duration": (datetime.now() - start_time).total_seconds()
            }
            
        except Exception as e:
            raise ScaffoldError(f"Failed to create project: {e}")
    
    def create_section(self, section_config: Dict[str, Any]) -> None:
        """Create a single section."""
        section_name = section_config["name"]
        section_folder = self.project_folder / f"{self.project_code}_sec{section_name}"
        
        # Create section directories
        section_folder.mkdir(exist_ok=True)
        (section_folder / "inputs").mkdir(exist_ok=True)
        (section_folder / "outputs").mkdir(exist_ok=True)
        (section_folder / "logs").mkdir(exist_ok=True)
        
        # Generate provenance ID
        provenance_id = self.file_tracker.generate_provenance_id(section_name)
        
        # Add section to manifest
        self.manifest.add_section(section_name, {
            "folder": str(section_folder.relative_to(self.project_folder)),
            "inputs": section_config.get("inputs", []),
            "outputs": section_config.get("outputs", [])
        }, provenance_id)
        
        # Create placeholder files
        self._create_section_files(section_folder, section_config, section_name)
        
        # Create section README
        self._create_section_readme(section_folder, section_name, provenance_id)
        
        # Create run scripts based on language preference
        language = self.config.get("project.language", "python")
        if language in ["python", "both"]:
            self._create_run_script(section_folder, section_name)
        if language in ["r", "both"]:
            self._create_run_r_script(section_folder, section_name)
        
        self.created_sections.append({
            "name": section_name,
            "folder": str(section_folder),
            "provenance_id": provenance_id,
            "input_count": len(section_config.get("inputs", [])),
            "output_count": len(section_config.get("outputs", []))
        })
    
    def _create_section_files(self, section_folder: Path, section_config: Dict[str, Any], 
                            section_name: str) -> None:
        """Create placeholder files for a section."""
        # Get available placeholders
        placeholders = self.config.get("placeholders", {})
        
        # Add default project placeholder
        if "proj" not in placeholders:
            placeholders["proj"] = self.project_code
        
        # Create input files
        inputs = section_config.get("inputs", [])
        for pattern in inputs:
            self._create_file_from_pattern(
                section_folder / "inputs", 
                pattern, 
                placeholders,
                "input", 
                section_name
            )
        
        # Create output files
        outputs = section_config.get("outputs", [])
        for pattern in outputs:
            self._create_file_from_pattern(
                section_folder / "outputs", 
                pattern, 
                placeholders,
                "output", 
                section_name
            )
    
    def _create_file_from_pattern(self, base_folder: Path, pattern: str, 
                                placeholders: Dict[str, str], file_type: str,
                                section_name: str) -> None:
        """Create file from pattern with placeholders."""
        # Handle glob patterns - create only one example file
        if "*" in pattern or "?" in pattern:
            # Extract the base directory if specified
            base_parts = pattern.split("/")
            if len(base_parts) > 1:
                dir_part = "/".join(base_parts[:-1])
                dir_folder = base_folder / dir_part
                dir_folder.mkdir(parents=True, exist_ok=True)
            
            # Create example file with simplified pattern
            example_pattern = pattern.replace("*", "example").replace("?", "x")
            example_file = base_folder / example_pattern
            
            # Ensure parent directories exist
            if not example_file.parent.exists():
                example_file.parent.mkdir(parents=True)
            
            # Create placeholder file
            with open(example_file, 'w') as f:
                f.write(f"# Placeholder file for pattern: {pattern}\n")
                f.write(f"# Created: {datetime.now().isoformat()}\n")
                f.write(f"# Section: {section_name}\n")
                f.write(f"# Type: {file_type}\n")
            
            self.created_files.append({
                "path": str(example_file),
                "section": section_name,
                "type": file_type,
                "pattern": pattern
            })
        else:
            # Regular file pattern
            try:
                # Apply placeholders if any
                file_name = pattern
                if placeholders and ("{" in pattern and "}" in pattern):
                    file_name = self.expand_pattern(pattern, placeholders)
                
                # Create the file
                file_path = base_folder / file_name
                
                # Ensure parent directories exist
                if not file_path.parent.exists():
                    file_path.parent.mkdir(parents=True)
                
                # Create placeholder file
                with open(file_path, 'w') as f:
                    f.write(f"# Placeholder file\n")
                    f.write(f"# Created: {datetime.now().isoformat()}\n")
                    f.write(f"# Section: {section_name}\n")
                    f.write(f"# Type: {file_type}\n")
                
                self.created_files.append({
                    "path": str(file_path),
                    "section": section_name,
                    "type": file_type,
                    "pattern": pattern
                })
            except Exception as e:
                print(f"Warning: Failed to create file from pattern '{pattern}': {e}")
    
    def create_sandbox(self, items: List[str]) -> None:
        """Create sandbox items."""
        sandbox_folder = self.project_folder / "lda_sandbox"
        sandbox_folder.mkdir(exist_ok=True)
        
        for item in items:
            item_folder = sandbox_folder / item
            item_folder.mkdir(exist_ok=True)
            
            # Create draft file
            draft_file = item_folder / f"{item}_draft.md"
            draft_file.touch()
            
            self.created_files.append({
                "path": str(draft_file),
                "section": "sandbox",
                "type": "sandbox",
                "pattern": None
            })
    
    def _create_section_readme(self, section_folder: Path, section_name: str, 
                             provenance_id: str) -> None:
        """Create README for a section."""
        # Prepare context for template
        context = {
            "section_name": section_name,
            "creation_time": datetime.now().isoformat(),
            "provenance_id": provenance_id,
            "analyst": self.config.get("project.analyst", "Unknown")
        }
        
        # Generate and write the README using the template service
        readme_path = section_folder / "README.md"
        self.template_service.write_template(
            "readme/section_readme.md.j2",
            readme_path,
            context
        )
    
    def _create_run_script(self, section_folder: Path, section_name: str) -> None:
        """Create run.py script for a section."""
        # Prepare context for template
        context = {
            "section_name": section_name,
            "project_name": self.config.get("project.name", "LDA Project"),
            "creation_time": datetime.now().isoformat(),
            "timestamp": datetime.now().strftime('%Y%m%d_%H%M%S')
        }
        
        # Generate and write the script using the template service
        run_path = section_folder / "run.py"
        self.template_service.write_template(
            "scripts/python_run.py.j2",
            run_path,
            context
        )
        
        # Make executable on Unix systems
        os.chmod(run_path, 0o755)
        
        self.created_files.append({
            "path": str(run_path),
            "section": section_name,
            "type": "script",
            "pattern": None
        })
    
    def create_project_files(self) -> None:
        """Create project-level files."""
        # Prepare context for the project README template
        context = {
            "project_name": self.config.get("project.name", "LDA Project"),
            "analyst": self.config.get("project.analyst", "Unknown"),
            "creation_time": datetime.now().isoformat(),
            "sections": self.created_sections
        }
        
        # Generate and write the README using the template service
        readme_path = self.project_folder / "README.md"
        self.template_service.write_template(
            "readme/project_readme.md.j2",
            readme_path,
            context
        )
    
    def validate_placeholders(self, pattern: str, available_placeholders: Dict[str, str]) -> List[str]:
        """Validate placeholder usage in patterns."""
        required_placeholders = re.findall(r"\{([^}]+)\}", pattern)
        missing = [p for p in required_placeholders if p not in available_placeholders]
        return missing
    
    def expand_pattern(self, pattern: str, placeholders: Dict[str, str]) -> str:
        """Expand pattern with placeholder values."""
        try:
            return pattern.format(**placeholders)
        except KeyError as e:
            raise MissingPlaceholderError([str(e).strip("'")], pattern)
    
    def create_playground(self) -> None:
        """Create the LDA playground directory."""
        playground_folder = self.project_folder / "lda_playground"
        playground_folder.mkdir(exist_ok=True)
        
        # Create subdirectories
        (playground_folder / "experiments").mkdir(exist_ok=True)
        (playground_folder / "scratch").mkdir(exist_ok=True)
        (playground_folder / "notebooks").mkdir(exist_ok=True)
        
        # Prepare context for the playground README template
        context = {
            "project_name": self.config.get("project.name", "LDA Project"),
            "creation_time": datetime.now().isoformat()
        }
        
        # Generate and write the README using the template service
        readme_path = playground_folder / "README.md"
        self.template_service.write_template(
            "readme/playground_readme.md.j2",
            readme_path,
            context
        )
        
        # Create example scripts
        language = self.config.get("project.language", "python")
        if language in ["python", "both"]:
            self._create_playground_python_example(playground_folder)
        if language in ["r", "both"]:
            self._create_playground_r_example(playground_folder)
    
    def _create_playground_python_example(self, playground_folder: Path) -> None:
        """Create example Python script for playground."""
        # Prepare context for the playground Python example template
        context = {
            "project_name": self.config.get("project.name", "LDA Project"),
            "creation_time": datetime.now().isoformat()
        }
        
        # Create the parent directory if it doesn't exist
        script_path = playground_folder / "experiments" / "explore.py"
        script_path.parent.mkdir(exist_ok=True)
        
        # Generate and write the script using the template service
        self.template_service.write_template(
            "scripts/python_playground.py.j2",
            script_path,
            context
        )
        
        self.created_files.append({
            "path": str(script_path),
            "section": "playground",
            "type": "script",
            "pattern": None
        })
    
    def _create_playground_r_example(self, playground_folder: Path) -> None:
        """Create example R script for playground."""
        # Prepare context for template
        context = {
            "project_name": self.config.get("project.name", "LDA Project"),
            "creation_time": datetime.now().isoformat()
        }
        
        # Create the parent directory if it doesn't exist
        script_path = playground_folder / "experiments" / "explore.R"
        script_path.parent.mkdir(exist_ok=True)
        
        # Generate and write the script using the template service
        self.template_service.write_template(
            "scripts/r_playground.R.j2",
            script_path,
            context
        )
        
        self.created_files.append({
            "path": str(script_path),
            "section": "playground",
            "type": "script",
            "pattern": None
        })
    
    def _create_run_r_script(self, section_folder: Path, section_name: str) -> None:
        """Create run.R script for a section."""
        # Prepare context for template
        context = {
            "section_name": section_name,
            "project_name": self.config.get("project.name", "LDA Project"),
            "creation_time": datetime.now().isoformat()
        }
        
        # Generate and write the script using the template service
        run_path = section_folder / "run.R"
        self.template_service.write_template(
            "scripts/r_run.R.j2",
            run_path,
            context
        )
        
        # Make executable on Unix systems
        os.chmod(run_path, 0o755)
        
        self.created_files.append({
            "path": str(run_path),
            "section": section_name,
            "type": "script",
            "pattern": None
        })
        
    def save_project_config(self) -> None:
        """Save configuration file inside the project folder."""
        # Save config file in project root
        config_file_path = self.project_folder / "lda_config.yaml"
        self.config.save(str(config_file_path))
        
        # Create .lda directory for internal state
        (self.project_folder / ".lda").mkdir(exist_ok=True)
        
        self.created_files.append({
            "path": str(config_file_path),
            "section": "project",
            "type": "config",
            "pattern": None
        })