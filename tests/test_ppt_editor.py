"""Unit tests for PPT editor functionality."""
import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch
from src.report_generator.ppt_editor import PPTEditor
from src.report_generator.config import ReportConfig

class TestPPTEditor:
    """Test PPT editor functionality."""
    
    def test_replace_text_in_slide(self):
        """Test text replacement in slide."""
        # Mock presentation and slide structure
        mock_run = Mock()
        mock_run.text = "Hello MPE, decrease is decrease_percent on date"
        
        mock_paragraph = Mock()
        mock_paragraph.runs = [mock_run]
        
        mock_text_frame = Mock()
        mock_text_frame.paragraphs = [mock_paragraph]
        
        mock_shape = Mock()
        mock_shape.text_frame = mock_text_frame
        
        mock_slide = Mock()
        mock_slide.shapes = [mock_shape]
        
        mock_presentation = Mock()
        mock_presentation.slides = [mock_slide]
        
        # Test replacement
        editor = PPTEditor(Path("dummy.pptx"))
        editor.presentation = mock_presentation
        
        replacements = {
            "MPE": "$120 B",
            "decrease_percent": "3.5%",
            "date": "August 2025"
        }
        
        editor.replace_text_in_slide(1, replacements)
        
        expected = "Hello $120 B, decrease is 3.5% on August 2025"
        assert mock_run.text == expected
    
    def test_invalid_slide_number(self):
        """Test error handling for invalid slide number."""
        mock_presentation = Mock()
        mock_presentation.slides = []
        
        editor = PPTEditor(Path("dummy.pptx"))
        editor.presentation = mock_presentation
        
        with pytest.raises(ValueError, match="Slide 1 does not exist"):
            editor.replace_text_in_slide(1, {})
    
    @patch('src.report_generator.ppt_editor.Presentation')
    def test_load_presentation(self, mock_presentation_class):
        """Test presentation loading."""
        mock_pres = Mock()
        mock_pres.slides = [Mock(), Mock()]
        mock_presentation_class.return_value = mock_pres
        
        editor = PPTEditor(Path("test.pptx"))
        editor.load_presentation()
        
        assert editor.presentation == mock_pres
        mock_presentation_class.assert_called_once_with(Path("test.pptx"))