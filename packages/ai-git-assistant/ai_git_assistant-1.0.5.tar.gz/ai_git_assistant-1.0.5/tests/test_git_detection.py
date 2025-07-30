import pytest
import subprocess
import os
from pathlib import Path
from ai_git_assistant.__main__ import find_git_root

def test_find_git_root(tmp_path):
    repo_path = tmp_path / "test_repo"
    repo_path.mkdir()
    subprocess.run(["git", "init"], cwd=repo_path)

    os.chdir(repo_path) 
    
    assert find_git_root() == repo_path.resolve()

    subdir = repo_path / "subdir"
    subdir.mkdir()
    os.chdir(subdir)
    assert find_git_root() == repo_path.resolve()

def test_not_a_git_repo(tmp_path):
    os.chdir(tmp_path)
    assert find_git_root() is None