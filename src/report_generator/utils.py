"""Utility functions for safe file operations."""
import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Union

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to prevent directory traversal."""
    return re.sub(r'[^\w\-_\.]', '_', filename)

def generate_timestamp() -> str:
    """Generate timestamp in YYYYMMDD_HHMMSS format."""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

def safe_path(base_dir: Path, filename: str) -> Path:
    """Create safe path within base directory."""
    safe_name = sanitize_filename(filename)
    path = base_dir / safe_name
    
    # Ensure path is within base directory
    if not str(path.resolve()).startswith(str(base_dir.resolve())):
        raise ValueError("Path traversal detected")
    
    return path

def atomic_write(target_path: Path, content_source: Union[Path, bytes]) -> None:
    """Write file atomically using temporary file."""
    target_path.parent.mkdir(parents=True, exist_ok=True)
    
    with tempfile.NamedTemporaryFile(
        dir=target_path.parent,
        delete=False,
        suffix='.tmp'
    ) as tmp_file:
        if isinstance(content_source, Path):
            with open(content_source, 'rb') as src:
                tmp_file.write(src.read())
        else:
            tmp_file.write(content_source)
        
        tmp_path = Path(tmp_file.name)
    
    tmp_path.replace(target_path)