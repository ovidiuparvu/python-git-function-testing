import subprocess
from pathlib import Path


def current_branch(path: str | Path = '.') -> str | None:
    result = subprocess.run(
        ['git', 'rev-parse', '--abbrev-ref', 'HEAD'],
        cwd=path,
        capture_output=True,
        text=True,
        check=True
    )
    return result.stdout.strip()
