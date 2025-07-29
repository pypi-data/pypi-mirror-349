"""Test project name parser functionality."""

import pytest
from lda.core.name_parser import ProjectNameParser


class TestProjectNameParser:
    """Test smart project name parsing."""
    
    def test_parse_analyst_code_date_pattern(self):
        """Test parsing Analyst_ProjectCode_Date pattern."""
        result = ProjectNameParser.parse("Smith_ALS301_2024Q1")
        
        assert result['analyst'] == 'smith'
        assert result['code'] == 'ALS301'
        assert result['date'] == '2024Q1'
    
    def test_parse_code_analyst_date_pattern(self):
        """Test parsing ProjectCode_Analyst_Date pattern."""
        result = ProjectNameParser.parse("ALS301_Smith_2024")
        
        assert result['code'] == 'ALS301'
        assert result['analyst'] == 'smith'
        assert result['date'] == '2024'
    
    def test_parse_analyst_name_date_pattern(self):
        """Test parsing Analyst_ProjectName_Date pattern."""
        result = ProjectNameParser.parse("Johnson_DrugStudy_2024")
        
        assert result['analyst'] == 'johnson'
        assert result['name'] == 'DrugStudy'
        assert result['date'] == '2024'
    
    def test_parse_code_site_date_pattern(self):
        """Test parsing ProjectCode-SiteCode-Date pattern."""
        result = ProjectNameParser.parse("ALS301-BOS-2024")
        
        assert result['code'] == 'ALS301'
        assert result['site'] == 'BOS'
        assert result['date'] == '2024'
    
    def test_parse_study_phase_year_pattern(self):
        """Test parsing StudyName_Phase_Year pattern."""
        result = ProjectNameParser.parse("Alzheimer_Phase3_2024")
        
        assert result['name'] == 'Alzheimer'
        assert result['phase'] == '3'
        assert result['date'] == '2024'
    
    def test_general_extraction(self):
        """Test general extraction when no pattern matches."""
        result = ProjectNameParser.parse("My Research Project 2024")
        
        assert result['date'] == '2024'
        assert result['name'] == 'My Research Project 2024'
    
    def test_suggest_values_with_confidence(self):
        """Test value suggestions with confidence scores."""
        suggestions, confidence = ProjectNameParser.suggest_values("Smith_ALS301_2024")
        
        assert suggestions['analyst'] == 'smith'
        assert suggestions['code'] == 'ALS301'
        assert confidence > 0.5
    
    def test_format_project_code_simple(self):
        """Test simple project code generation."""
        code = ProjectNameParser.format_project_code("MyProject")
        assert code == "MYPROJECT"
    
    def test_format_project_code_multi_word(self):
        """Test project code generation from multi-word names."""
        code = ProjectNameParser.format_project_code("Climate Change Study")
        assert code == "CCS"
    
    def test_format_project_code_long_name(self):
        """Test project code generation from long names."""
        code = ProjectNameParser.format_project_code("Very Long Research Project Name")
        assert code == "VLRP"
    
    def test_format_project_code_with_numbers(self):
        """Test project code generation with numbers."""
        code = ProjectNameParser.format_project_code("Study 2024")
        assert code == "S2024"
    
    def test_post_processing_analyst_cleanup(self):
        """Test analyst name post-processing."""
        result = ProjectNameParser.parse("Dr_Smith_Study_2024")
        assert result['analyst'] == 'smith'  # Title removed, lowercase
    
    def test_empty_name_handling(self):
        """Test handling of empty project names."""
        result = ProjectNameParser.parse("")
        assert result['name'] is None or result['name'] == ""
    
    def test_special_characters_handling(self):
        """Test handling of special characters."""
        result = ProjectNameParser.parse("Project@Home_2024")
        assert result['date'] == '2024'
    
    def test_quarterly_date_extraction(self):
        """Test extraction of quarterly dates."""
        result = ProjectNameParser.parse("Study_2024Q2")
        assert result['date'] == '2024'  # Q2 stripped in post-processing