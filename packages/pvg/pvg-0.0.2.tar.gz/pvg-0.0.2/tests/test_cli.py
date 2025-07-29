import os
import json
import pytest
from click.testing import CliRunner
from pvg.cli import cli, get_cache_dir, safe_path
from unittest.mock import patch, call

@pytest.fixture
def runner():
    """Create a CLI test runner."""
    return CliRunner()

def test_cli_help(runner):
    """Test the CLI help output."""
    result = runner.invoke(cli, ['--help'])
    assert result.exit_code == 0
    assert 'PVG - pip-via-git' in result.output

def test_install_help(runner):
    """Test the install command help output."""
    result = runner.invoke(cli, ['install', '--help'])
    assert result.exit_code == 0
    assert 'Install a package from the specified source' in result.output

@pytest.mark.integration
def test_install_command(runner, temp_cache_dir, mock_git_repo):
    """Test the install command with a mock repository."""
    git_url = "https://github.com/test/repo.git"
    repo_hash = safe_path(git_url)
    expected_repo_path = os.path.join(temp_cache_dir, repo_hash, "repo")
    
    # Mock subprocess.run to avoid actual git and pip commands
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        result = runner.invoke(cli, ['install', git_url])
        
        assert result.exit_code == 0
        assert 'Installing package from' in result.output
        assert 'Installation successful!' in result.output
        
        # Verify git clone was called correctly
        clone_call = mock_run.call_args_list[0]
        assert clone_call == call(
            ['git', 'clone', git_url, expected_repo_path],
            check=True,
            capture_output=True,
            text=True
        )

@pytest.mark.integration
def test_install_with_force(runner, temp_cache_dir, mock_git_repo):
    """Test the install command with force flag."""
    git_url = "https://github.com/test/repo.git"
    repo_hash = safe_path(git_url)
    expected_repo_path = os.path.join(temp_cache_dir, repo_hash, "repo")
    
    # Create the repo directory to simulate existing installation
    os.makedirs(os.path.join(temp_cache_dir, repo_hash, "repo"), exist_ok=True)
    
    # Mock subprocess.run to avoid actual git and pip commands
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        
        # Force reinstall
        result = runner.invoke(cli, ['install', '--force', git_url])
        assert result.exit_code == 0
        assert 'Force flag used' in result.output
        
        # Verify git clone was called with correct path
        clone_call = mock_run.call_args_list[0]
        assert clone_call == call(
            ['git', 'clone', git_url, expected_repo_path],
            check=True,
            capture_output=True,
            text=True
        )

def test_clean_cache_command(runner, temp_cache_dir):
    """Test the clean-cache command."""
    # Create some content in cache
    os.makedirs(os.path.join(temp_cache_dir, 'test-dir'))
    
    # Test with 'no' response
    result = runner.invoke(cli, ['clean-cache'], input='n\n')
    assert result.exit_code == 0
    assert os.path.exists(temp_cache_dir)
    
    # Test with 'yes' response
    result = runner.invoke(cli, ['clean-cache'], input='y\n')
    assert result.exit_code == 0
    assert not os.path.exists(temp_cache_dir)

def test_list_cache_command(runner, temp_cache_dir):
    """Test the list-cache command."""
    # Test empty cache
    result = runner.invoke(cli, ['list-cache'])
    assert result.exit_code == 0
    
    # Create a mock cached package
    package_dir = os.path.join(temp_cache_dir, 'test-hash')
    os.makedirs(package_dir)
    meta_info = {
        "git_url": "https://github.com/test/repo.git",
        "installed_at": "2024-01-01",
        "last_updated": "2024-01-01"
    }
    with open(os.path.join(package_dir, 'meta.json'), 'w') as f:
        json.dump(meta_info, f)
    
    # Test with cached package
    result = runner.invoke(cli, ['list-cache'])
    assert result.exit_code == 0
    assert 'https://github.com/test/repo.git' in result.output 