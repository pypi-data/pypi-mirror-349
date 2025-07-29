"""Template service for LDA project.

This module provides a template service for rendering project templates
using Jinja2.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import pkg_resources

from jinja2 import Environment, FileSystemLoader, select_autoescape, Template


class TemplateService:
    """Service for rendering templates using Jinja2."""

    def __init__(self):
        """Initialize the template service."""
        # Get the path to the templates directory
        template_dir = Path(__file__).parent.parent / "templates"
        
        # Set up Jinja2 environment
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True,
        )
    
    def render_template(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template with the given context.
        
        Args:
            template_name: Name of the template file
            context: Dictionary of context variables
            
        Returns:
            str: The rendered template
        """
        template = self.env.get_template(template_name)
        return template.render(**context)
    
    def render_string(self, template_string: str, context: Dict[str, Any]) -> str:
        """Render a template string with the given context.
        
        Args:
            template_string: The template string to render
            context: Dictionary of context variables
            
        Returns:
            str: The rendered template
        """
        template = self.env.from_string(template_string)
        return template.render(**context)
    
    def write_template(self, 
                     template_name: str, 
                     output_file: Path, 
                     context: Dict[str, Any],
                     create_dirs: bool = True) -> None:
        """Render a template and write it to a file.
        
        Args:
            template_name: Name of the template file
            output_file: Path to the output file
            context: Dictionary of context variables
            create_dirs: Whether to create parent directories
        """
        content = self.render_template(template_name, context)
        
        # Create parent directory if it doesn't exist
        if create_dirs and not output_file.parent.exists():
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
        # Write the rendered template to the file
        output_file.write_text(content)
    
    def write_string_template(self, 
                            template_string: str, 
                            output_file: Path, 
                            context: Dict[str, Any],
                            create_dirs: bool = True) -> None:
        """Render a template string and write it to a file.
        
        Args:
            template_string: The template string to render
            output_file: Path to the output file
            context: Dictionary of context variables
            create_dirs: Whether to create parent directories
        """
        content = self.render_string(template_string, context)
        
        # Create parent directory if it doesn't exist
        if create_dirs and not output_file.parent.exists():
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
        # Write the rendered template to the file
        output_file.write_text(content)