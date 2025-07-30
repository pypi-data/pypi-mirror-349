import pytest
from ai_git_assistant.__main__ import add_files
from unittest.mock import patch

def test_add_files_success():
    with patch('subprocess.run') as mock_run:
        mock_run.return_value = MagicMock(returncode=0)
        result = add_files(["test_file.txt"])
        assert "exitosa" in result 