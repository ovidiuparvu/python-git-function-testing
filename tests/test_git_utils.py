import os
import subprocess
from pathlib import Path
import pytest
from src.git import get_current_branch

@pytest.fixture
def temp_git_repo(tmp_path):
    """Create a temporary git repository for testing."""
    # Initialize git repo
    subprocess.run(['git', 'init'], cwd=tmp_path, check=True)
    
    # Configure git user for commits
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], cwd=tmp_path)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], cwd=tmp_path)
    
    # Create and commit a file
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    subprocess.run(['git', 'add', 'test.txt'], cwd=tmp_path)
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], cwd=tmp_path)
    
    return tmp_path

def test_get_current_branch_main(temp_git_repo):
    """Test getting branch name from a new repository (should be main/master)."""
    branch = get_current_branch(temp_git_repo)
    assert branch in ['main', 'master']

def test_get_current_branch_new_branch(temp_git_repo):
    """Test getting branch name after creating and checking out a new branch."""
    subprocess.run(['git', 'checkout', '-b', 'feature'], cwd=temp_git_repo)
    assert get_current_branch(temp_git_repo) == 'feature'

def test_get_current_branch_non_git_directory(tmp_path):
    """Test behavior in a non-git directory."""
    assert get_current_branch(tmp_path) is None

def test_get_current_branch_relative_path():
    """Test with relative path (current directory)."""
    branch = get_current_branch()
    assert isinstance(branch, str) or branch is None
