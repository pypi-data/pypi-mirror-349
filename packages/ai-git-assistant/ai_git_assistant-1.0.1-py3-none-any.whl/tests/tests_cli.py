from unittest.mock import patch, MagicMock
from ai_git_assistant.__main__ import git_status_info, add_info

def test_git_status_info():
    with patch('subprocess.run') as mock_run:
        # Configura mock para simular salida de git
        mock_run.return_value = MagicMock(stdout="file1.txt\nfile2.txt")
        
        result = git_status_info()
        assert isinstance(result, dict)
        assert "unstaged" in result
        assert result["unstaged"] == ["file1.txt", "file2.txt"]