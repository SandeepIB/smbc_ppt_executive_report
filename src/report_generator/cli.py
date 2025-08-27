"""Command-line interface for PPT report generator."""
import argparse
import logging
import sys
from pathlib import Path
from .config import load_config
from .ppt_editor import PPTEditor

def setup_logging():
    """Configure structured logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description='Generate PPT reports from JSON config')
    parser.add_argument('--config', required=True, help='Path to config JSON file')
    parser.add_argument('--input', required=True, help='Path to input PPTX file')
    parser.add_argument('--output-dir', required=True, help='Output directory')
    
    args = parser.parse_args()
    setup_logging()
    logger = logging.getLogger(__name__)
    
    try:
        # Validate paths
        config_path = Path(args.config)
        input_path = Path(args.input)
        output_dir = Path(args.output_dir)
        
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found: {config_path}")
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
        
        # Load configuration
        config = load_config(config_path)
        
        # Process presentation
        editor = PPTEditor(input_path)
        editor.load_presentation()
        editor.replace_text_in_slide(config.slide_number, config.replacements)
        
        # Save output
        output_path = editor.save_report(output_dir)
        print(f"Report generated: {output_path}")
        
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()