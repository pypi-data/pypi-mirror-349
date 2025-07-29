"""Smart project name parser for LDA."""

import re
from typing import Dict, Optional, Tuple
from datetime import datetime


class ProjectNameParser:
    """Extracts project metadata from naming conventions."""
    
    # Common patterns found in research project names
    PATTERNS = [
        # Pattern: SiteCode_StudyCode_Condition_Week
        # Example: CN111_SPG302_REST_WK8
        r'^(?P<site>[A-Z]+\d*)_(?P<study>[A-Z]+\d+)_(?P<condition>[A-Z]+)_(?P<week>WK\d+)$',
        
        # Pattern: Analyst_ProjectCode_Date
        # Example: Smith_ALS301_2024Q1
        r'^(?P<analyst>[A-Za-z]+)_(?P<code>[A-Z0-9]+)_(?P<date>\d{4}Q?\d*)$',
        
        # Pattern: ProjectCode_Analyst_Date
        # Example: ALS301_Smith_2024
        r'^(?P<code>[A-Z0-9]+)_(?P<analyst>[A-Za-z]+)_(?P<date>\d{4})$',
        
        # Pattern: Analyst_ProjectName_Date
        # Example: Johnson_DrugStudy_2024
        r'^(?P<analyst>[A-Za-z]+)_(?P<name>[A-Za-z]+)_(?P<date>\d{4})$',
        
        # Pattern: ProjectCode-SiteCode-Date
        # Example: ALS301-BOS-2024
        r'^(?P<code>[A-Z0-9]+)-(?P<site>[A-Z]+)-(?P<date>\d{4})$',
        
        # Pattern: StudyName_Phase_Year
        # Example: Alzheimer_Phase3_2024
        r'^(?P<name>[A-Za-z]+)_Phase(?P<phase>\d)_(?P<date>\d{4})$',
    ]
    
    # Common researcher name prefixes
    NAME_PREFIXES = ['Dr', 'Prof', 'Mr', 'Ms', 'Mrs']
    
    @classmethod
    def parse(cls, project_name: str) -> Dict[str, Optional[str]]:
        """Parse project name and extract metadata."""
        result = {
            'analyst': None,
            'code': None,
            'date': None,
            'name': None,
            'phase': None,
            'site': None,
            'study': None,
            'condition': None,
            'week': None
        }
        
        # Clean the name
        clean_name = project_name.strip()
        
        # Try each pattern
        for pattern in cls.PATTERNS:
            match = re.match(pattern, clean_name)
            if match:
                result.update(match.groupdict())
                break
        
        # If no pattern matches, try more general extraction
        if not any(result.values()):
            result.update(cls._extract_general(clean_name))
        
        # Post-process extracted values
        result = cls._post_process(result, clean_name)
        
        return result
    
    @classmethod
    def _extract_general(cls, name: str) -> Dict[str, Optional[str]]:
        """Extract metadata using general heuristics."""
        result = {}
        parts = re.split(r'[-_\s]+', name)
        
        for part in parts:
            # Check for year
            if re.match(r'^\d{4}$', part):
                result['date'] = part
            # Check for project code (all caps with numbers)
            elif re.match(r'^[A-Z]+\d+$', part):
                result['code'] = part
            # Check for phase
            elif re.match(r'^[Pp]hase\d$', part):
                result['phase'] = part[-1]
            # Check for researcher names
            elif part.title() in cls.NAME_PREFIXES:
                # Next part might be the name
                idx = parts.index(part)
                if idx + 1 < len(parts):
                    result['analyst'] = parts[idx + 1]
        
        return result
    
    @classmethod
    def _post_process(cls, result: Dict[str, Optional[str]], original: str) -> Dict[str, Optional[str]]:
        """Clean up and validate extracted values."""
        # Clean analyst name
        if result.get('analyst'):
            analyst = result['analyst']
            # Remove titles
            for prefix in cls.NAME_PREFIXES:
                analyst = analyst.replace(prefix, '').strip()
            # Convert to lowercase username format
            result['analyst'] = analyst.lower()
        
        # Generate project code if not found
        if not result.get('code') and original:
            # Create code from name
            words = re.findall(r'[A-Z][a-z]+|[A-Z]+(?=[A-Z][a-z]|\b)', original)
            if words:
                result['code'] = ''.join(w[:3].upper() for w in words[:2])
            else:
                result['code'] = re.sub(r'[^A-Za-z0-9]', '', original)[:6].upper()
        
        # Ensure date is in standard format
        if result.get('date'):
            date_str = result['date']
            # Convert Q format to year only
            if 'Q' in date_str:
                result['date'] = date_str[:4]
        
        # Set the project name if not extracted
        if not result.get('name'):
            result['name'] = original
        
        return result
    
    @classmethod
    def suggest_values(cls, project_name: str) -> Tuple[Dict[str, Optional[str]], float]:
        """Parse name and return suggestions with confidence score."""
        suggestions = cls.parse(project_name)
        
        # Calculate confidence based on how many fields were extracted
        extracted_count = sum(1 for v in suggestions.values() if v is not None)
        total_fields = len(suggestions)
        confidence = extracted_count / total_fields
        
        return suggestions, confidence
    
    @classmethod
    def format_project_code(cls, name: str) -> str:
        """Generate a project code from a project name."""
        # Remove special characters and split into words
        words = re.findall(r'\b\w+\b', name)
        
        if not words:
            return "PROJ"
        
        # If the name is short, use it as-is (cleaned)
        if len(words) == 1 and len(words[0]) <= 8:
            return words[0].upper()
        
        # Otherwise, create an acronym
        acronym = ''.join(word[0].upper() for word in words[:4])
        
        # If acronym is too short, add numbers
        if len(acronym) < 3:
            acronym += datetime.now().strftime("%y")
        
        return acronym