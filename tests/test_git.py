import os
import subprocess
from pathlib import Path
import pytest
from git_function_testing.git import current_branch
from _pytest.fixtures import FixtureRequest
from typing import Generator

@pytest.fixture
def temp_git_repo(tmp_path: Path) -> Path:
    os.chdir(tmp_path)
    subprocess.run(['git', 'init'], check=True)
    subprocess.run(['git', 'config', 'user.name', 'Test User'], check=True)
    subprocess.run(['git', 'config', 'user.email', 'test@example.com'], check=True)
    
    test_file = tmp_path / "test.txt"
    test_file.write_text("test content")
    subprocess.run(['git', 'add', '.'], check=True)
    subprocess.run(['git', 'commit', '-m', 'Initial commit'], check=True)
    
    return tmp_path

def test_current_branch_main(temp_git_repo: Path) -> None:
    assert current_branch(temp_git_repo) in ['main', 'master']

def test_current_branch_new_branch(temp_git_repo: Path) -> None:
    subprocess.run(['git', 'checkout', '-b', 'feature-branch'], check=True)
    assert current_branch(temp_git_repo) == 'feature-branch'

def test_current_branch_with_path_object(temp_git_repo: Path) -> None:
    path = Path(temp_git_repo)
    assert current_branch(path) in ['main', 'master']

def test_current_branch_non_git_dir(tmp_path: Path) -> None:
    assert current_branch(tmp_path) is None

def test_current_branch_current_dir(temp_git_repo: Path) -> None:
    os.chdir(temp_git_repo)
    assert current_branch() in ['main', 'master']

def test_current_branch_detached_head(temp_git_repo: Path) -> None:
    result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                          capture_output=True, text=True, check=True)
    commit_hash = result.stdout.strip()
    
    subprocess.run(['git', 'checkout', commit_hash], check=True)
    
    assert current_branch(temp_git_repo) == 'HEAD'
