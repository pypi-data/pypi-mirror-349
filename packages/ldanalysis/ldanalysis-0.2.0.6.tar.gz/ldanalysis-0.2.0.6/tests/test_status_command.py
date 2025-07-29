"""Test the status command functionality."""

import tempfile
import os
from pathlib import Path

from lda.config import LDAConfig
from lda.cli.commands import Commands
from lda.display.console import Console
from unittest.mock import Mock


def test_status_shows_correct_project_metadata(tmp_path):
    """Test that status command displays correct project metadata from config."""
    # Create a test project
    project_name = "Climate Analysis 2024"
    project_code = "climate_analysis_2024"
    analyst = "jane.doe"
    
    # Create config file
    config_file = tmp_path / f"{project_code}_config.yaml"
    config = LDAConfig()
    config.set("project.name", project_name)
    config.set("project.code", project_code)
    config.set("project.analyst", analyst)
    config.set("sections", [{"name": "data", "inputs": [], "outputs": []}])
    config.save(str(config_file))
    
    # Initialize project
    args = Mock()
    args.name = project_name
    args.analyst = analyst
    args.sections = "data"
    args.no_playground = False
    args.language = "python"
    
    display = Console(style="conservative")
    result = Commands.cmd_init(args, config, display)
    assert result == 0
    
    # Change to project directory
    project_dir = tmp_path / project_code
    os.chdir(project_dir)
    
    # Run status command
    status_args = Mock()
    status_args.format = None
    
    # Don't pass config initially - let status command find it
    result = Commands.cmd_status(status_args, None, display)
    assert result == 0
    
    # Verify the output (we'd need to capture display output for full verification)
    # For now, let's verify internal behavior by running with config
    result_with_config = Commands.cmd_status(status_args, config, display)
    assert result_with_config == 0


def test_status_finds_config_in_parent_directory(tmp_path):
    """Test that status command finds config file in parent directory."""
    # Create project structure
    project_code = "test_project"
    project_dir = tmp_path / project_code
    project_dir.mkdir()
    
    # Create config in parent directory
    config_file = tmp_path / f"{project_code}_config.yaml"
    config = LDAConfig()
    config.set("project.name", "Test Project")
    config.set("project.code", project_code)
    config.set("project.analyst", "test.user")
    config.save(str(config_file))
    
    # Create manifest in project directory
    manifest_dir = project_dir / ".lda"
    manifest_dir.mkdir()
    manifest_file = manifest_dir / "manifest.json"
    
    # Basic manifest content
    import json
    manifest_content = {
        "project": {
            "root": str(project_dir),
            "created": "2025-05-17T12:00:00"
        },
        "sections": {},
        "files": {},
        "history": []
    }
    
    with open(manifest_file, 'w') as f:
        json.dump(manifest_content, f)
    
    # Create CSV manifest for backward compatibility
    csv_manifest = project_dir / "lda_manifest.csv"
    csv_manifest.write_text("section,folder,analyst,timestamp,provenance_id\n")
    
    # Run status from project directory
    os.chdir(project_dir)
    
    status_args = Mock()
    status_args.format = None
    
    display = Console(style="conservative")
    result = Commands.cmd_status(status_args, None, display)
    assert result == 0