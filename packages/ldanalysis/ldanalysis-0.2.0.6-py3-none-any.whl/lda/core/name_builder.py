"""Universal project naming builder for LDA."""

import re
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
from ..display.console import Console


class NameField:
    """Configuration for a naming field."""
    
    def __init__(self, 
                 name: str,
                 prompt: str,
                 examples: List[str],
                 required: bool = False,
                 validator: Optional[callable] = None,
                 aliases: Optional[List[str]] = None,
                 transform: Optional[str] = None):
        """Initialize naming field configuration."""
        self.name = name
        self.prompt = prompt
        self.examples = examples
        self.required = required
        self.validator = validator or self._default_validator
        self.aliases = aliases or []
        self.transform = transform  # 'upper', 'lower', or None
    
    def _default_validator(self, value: str) -> Tuple[bool, Optional[str]]:
        """Default validation for field values."""
        if self.required and not value:
            return False, f"{self.name} is required"
        
        # Check for forbidden characters
        if value and re.search(r'[<>:"/\\|?*\s]', value):
            return False, f"Contains invalid characters. Spaces will be replaced with underscores."
        
        return True, None
    
    def validate(self, value: str) -> Tuple[bool, Optional[str]]:
        """Validate field value."""
        return self.validator(value)
    
    def prompt_text(self) -> str:
        """Get formatted prompt text."""
        status = "required" if self.required else "optional"
        examples_str = ", ".join(self.examples)
        return f"{self.prompt} (e.g., {examples_str}) [{status}]"
    
    def apply_transform(self, value: str) -> str:
        """Apply case transformation if configured."""
        if self.transform == 'upper':
            return value.upper()
        elif self.transform == 'lower':
            return value.lower()
        return value


class NameBuilder:
    """Interactive project name builder with field-based structure."""
    
    # Default field configuration
    DEFAULT_FIELDS = [
        NameField(
            name="project",
            prompt="Project/Study/Protocol",
            examples=["ALS301", "COVID19", "SensorX"],
            required=True,
            transform='upper'
        ),
        NameField(
            name="site",
            prompt="Site/Organization/Consortium",
            examples=["US", "LabA", "UCL"],
            required=False,
            aliases=["organization", "consortium"],
            transform='upper'
        ),
        NameField(
            name="cohort",
            prompt="Cohort/Arm/Group",
            examples=["Placebo", "Elderly", "Control"],
            required=False,
            aliases=["arm", "group"]
        ),
        NameField(
            name="phase",
            prompt="Phase/Session/Timepoint/Batch",
            examples=["6mo", "2024A", "Pre", "Phase3"],
            required=False,
            aliases=["session", "timepoint", "batch"]
        ),
        NameField(
            name="modality",
            prompt="Modality/DataType/Task/Platform",
            examples=["MRI", "RNAseq", "Stroop", "AWS"],
            required=False,
            aliases=["datatype", "task", "platform"]
        ),
        NameField(
            name="run",
            prompt="Run/Version/Analysis/Config",
            examples=["v2", "reanalysis", "HighGain"],
            required=False,
            aliases=["version", "analysis", "config"]
        ),
        NameField(
            name="custom",
            prompt="Custom/Qualifier/Freeform",
            examples=["pilot", "blinded", "final"],
            required=False,
            aliases=["qualifier", "freeform"]
        )
    ]
    
    def __init__(self, display: Console, fields: Optional[List[NameField]] = None):
        """Initialize name builder."""
        self.display = display
        self.fields = fields or self.DEFAULT_FIELDS
        self.values = {}
    
    def build_interactive(self, allow_override: bool = True) -> str:
        """Build project name interactively."""
        self.display.section("Let's build your project name")
        
        # Collect field values
        for i, field in enumerate(self.fields, 1):
            # Build current preview
            preview = self._build_preview()
            if preview:
                self.display.info(f"Preview: {preview}")
            
            # Prompt for field
            prompt = f"{i}. {field.prompt_text()}"
            response = input(f"{prompt}: ").strip()
            
            # Skip if empty and optional
            if not response and not field.required:
                print("[skip]")
                continue
            
            # Validate
            if response:
                is_valid, error = field.validate(response)
                if not is_valid:
                    self.display.error(error)
                    # For invalid characters, clean and continue
                    if "invalid characters" in error:
                        response = self._sanitize_value(response)
                        self.display.info(f"Using: {response}")
                    else:
                        # For other errors, retry
                        while not is_valid:
                            response = input(f"{prompt}: ").strip()
                            if not response and not field.required:
                                break
                            is_valid, error = field.validate(response)
                            if not is_valid:
                                self.display.error(error)
                
                if response:
                    # Apply field transformation if configured
                    transformed = field.apply_transform(response)
                    self.values[field.name] = transformed
        
        # Show final preview
        project_name = self._build_preview()
        self.display.section("Final Project Name")
        self.display.info(f"Preview: {project_name}")
        
        # Confirm or allow override
        response = input("\nIs this correct? [Y/n]: ").strip().lower()
        if response == 'n':
            if allow_override:
                custom_name = input("Enter custom project name (or press Enter to rebuild): ").strip()
                if custom_name:
                    return self._sanitize_value(custom_name)
                else:
                    # Rebuild
                    self.values = {}
                    return self.build_interactive(allow_override)
            else:
                # Rebuild
                self.values = {}
                return self.build_interactive(allow_override)
        
        return project_name
    
    def build_from_values(self, values: Dict[str, str]) -> str:
        """Build project name from provided values."""
        self.values = values
        return self._build_preview()
    
    def _build_preview(self) -> str:
        """Build current preview of project name."""
        parts = []
        for field in self.fields:
            if field.name in self.values and self.values[field.name]:
                parts.append(self.values[field.name])
        
        return "_".join(parts) if parts else ""
    
    def _sanitize_value(self, value: str) -> str:
        """Sanitize value for filesystem compatibility."""
        # Replace spaces with underscores
        value = value.replace(" ", "_")
        # Remove problematic characters
        value = re.sub(r'[<>:"/\\|?*]', '', value)
        return value
    
    def validate_length(self, name: str, max_length: int = 64) -> Tuple[bool, Optional[str]]:
        """Validate project name length."""
        if len(name) > max_length:
            return False, f"Name is too long ({len(name)} chars). Maximum is {max_length}."
        return True, None
    
    def check_uniqueness(self, name: str, directory: Path) -> Tuple[bool, Optional[str]]:
        """Check if project name is unique in directory."""
        potential_path = directory / name
        if potential_path.exists():
            return False, f"A project named '{name}' already exists in {directory}"
        return True, None
    
    def suggest_hierarchy(self, values: Dict[str, str]) -> Optional[str]:
        """Suggest hierarchical folder structure for deeply nested projects."""
        # If we have many fields filled, suggest hierarchy
        if len(values) > 4:
            # Create hierarchy from first few fields
            parts = []
            for field in self.fields[:3]:  # Use first 3 fields for hierarchy
                if field.name in values and values[field.name]:
                    parts.append(values[field.name])
            
            if len(parts) > 1:
                return "/".join(parts)
        
        return None


class NameTemplate:
    """Organizational naming template configuration."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize template from configuration."""
        self.name = config.get("name", "default")
        self.description = config.get("description", "")
        self.fields = self._parse_fields(config.get("fields", []))
        self.field_order = config.get("field_order", [])
        self.required_fields = config.get("required_fields", ["project"])
        self.aliases = config.get("aliases", {})
    
    def _parse_fields(self, field_configs: List[Dict[str, Any]]) -> List[NameField]:
        """Parse field configurations into NameField objects."""
        fields = []
        for config in field_configs:
            field = NameField(
                name=config["name"],
                prompt=config.get("prompt", config["name"]),
                examples=config.get("examples", []),
                required=config.get("required", False),
                aliases=config.get("aliases", []),
                transform=config.get("transform", None)
            )
            fields.append(field)
        return fields
    
    def get_builder(self, display: Console) -> NameBuilder:
        """Create a NameBuilder using this template."""
        return NameBuilder(display, fields=self.fields)
    
    @classmethod
    def load_from_file(cls, path: Path) -> 'NameTemplate':
        """Load template from YAML file."""
        import yaml
        
        try:
            with open(path) as f:
                config = yaml.safe_load(f)
            return cls(config)
        except Exception as e:
            raise ValueError(f"Failed to load template from {path}: {e}")
    
    @classmethod
    def get_default(cls) -> 'NameTemplate':
        """Get the default naming template."""
        default_config = {
            "name": "default",
            "description": "Default LDA naming template",
            "fields": [
                {
                    "name": "project",
                    "prompt": "Project/Study/Protocol",
                    "examples": ["ALS301", "COVID19", "SensorX"],
                    "required": True
                },
                {
                    "name": "site",
                    "prompt": "Site/Organization/Consortium",
                    "examples": ["US", "LabA", "UCL"],
                    "required": False,
                    "aliases": ["organization", "consortium"]
                },
                {
                    "name": "cohort",
                    "prompt": "Cohort/Arm/Group",
                    "examples": ["Placebo", "Elderly", "Control"],
                    "required": False,
                    "aliases": ["arm", "group"]
                },
                {
                    "name": "phase",
                    "prompt": "Phase/Session/Timepoint/Batch",
                    "examples": ["6mo", "2024A", "Pre", "Phase3"],
                    "required": False,
                    "aliases": ["session", "timepoint", "batch"]
                },
                {
                    "name": "modality",
                    "prompt": "Modality/DataType/Task/Platform",
                    "examples": ["MRI", "RNAseq", "Stroop", "AWS"],
                    "required": False,
                    "aliases": ["datatype", "task", "platform"]
                },
                {
                    "name": "run",
                    "prompt": "Run/Version/Analysis/Config",
                    "examples": ["v2", "reanalysis", "HighGain"],
                    "required": False,
                    "aliases": ["version", "analysis", "config"]
                },
                {
                    "name": "custom",
                    "prompt": "Custom/Qualifier/Freeform",
                    "examples": ["pilot", "blinded", "final"],
                    "required": False,
                    "aliases": ["qualifier", "freeform"]
                }
            ]
        }
        return cls(default_config)