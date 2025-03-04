import os
import subprocess
from pathlib import Path
import pytest
from src.git import get_current_branch
from _pytest.fixtures import FixtureRequest
from typing import Generator

@pytest.fixture
def temp_git_repo(tmp_path: Path) -> Path:
    """Create a temporary git repository with an initial commit."""
    os.chdir(tmp_path)
    subprocess.run(['git', 'init'], check=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True)
    
    # Create and commit a test file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
    
    return tmp_path

def test_get_current_branch_main(temp_git_repo: Path) -> None:
    """Test getting branch name from a git repository."""
    assert get_current_branch(temp_git_repo) in ['main', 'master']  # Different git versions use different defaults

def test_get_current_branch_new_branch(temp_git_repo: Path) -> None:
    """Test getting branch name after creating and switching to a new branch."""
    subprocess.run(['git', 'checkout', '-b', 'feature-branch'], check=True)
    assert get_current_branch(temp_git_repo) == 'feature-branch'

def test_get_current_branch_with_path_object(temp_git_repo: Path) -> None:
    """Test that the function works with Path objects."""
    path = Path(temp_git_repo)
    assert get_current_branch(path) in ['main', 'master']

def test_get_current_branch_non_git_dir(tmp_path: Path) -> None:
    """Test behavior in a non-git directory."""
    assert get_current_branch(tmp_path) is None

def test_get_current_branch_current_dir(temp_git_repo: Path) -> None:
    """Test getting branch name using default current directory."""
    os.chdir(temp_git_repo)
    assert get_current_branch() in ['main', 'master']

def test_get_current_branch_detached_head(temp_git_repo: Path) -> None:
    """Test behavior when HEAD is detached."""
    # Get current commit hash
    result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                          capture_output=True, text=True, check=True)
    commit_hash = result.stdout.strip()
    
    # Checkout the commit hash directly to create detached HEAD
    subprocess.run(['git', 'checkout', commit_hash], check=True)
    
    # Should still return the commit hash in detached HEAD state
    assert get_current_branch(temp_git_repo) == 'HEAD'
