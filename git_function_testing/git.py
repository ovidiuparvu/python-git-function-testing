import subprocess
from pathlib import Path
from typing import Optional

def get_current_branch(path: str | Path = '.') -> Optional[str]:
    """
    Get the current Git branch name for the specified directory.
    
    Args:
        path: Directory path to check (defaults to current directory)
    
    Returns:
        String containing branch name if successful, None if not a git repository
        or in case of errors
    """
    try:
        result = subprocess.run(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
            cwd=path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        return None
