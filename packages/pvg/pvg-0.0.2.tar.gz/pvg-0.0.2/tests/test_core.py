import os
import json
import pytest
from pathlib import Path
from unittest.mock import patch, call
from pvg.cli import (
    is_git_url,
    safe_path,
    get_cache_dir,
    write_meta_info,
    clone_or_pull
)

def test_is_git_url():
    """Test git URL detection."""
    assert is_git_url("https://github.com/user/repo.git")
    assert is_git_url("git@github.com:user/repo.git")
    assert is_git_url("git://github.com/user/repo.git")
    assert is_git_url("ssh://git@github.com/user/repo.git")
    
    assert not is_git_url("https://github.com/user/repo")
    assert not is_git_url("user/repo")
    assert not is_git_url("not-a-url")

def test_safe_path():
    """Test URL to safe path conversion."""
    url = "https://github.com/user/repo.git"
    path = safe_path(url)
    
    # Should be a hex string (SHA-256)
    assert len(path) == 64
    assert all(c in "0123456789abcdef" for c in path)
    
    # Same URL should produce same hash
    assert safe_path(url) == path
    
    # Different URLs should produce different hashes
    assert safe_path("https://github.com/other/repo.git") != path

def test_get_cache_dir(temp_cache_dir):
    """Test cache directory handling."""
    cache_dir = get_cache_dir()
    assert os.path.exists(cache_dir)
    assert os.path.isdir(cache_dir)

def test_write_meta_info(temp_cache_dir):
    """Test metadata writing."""
    package_dir = Path(temp_cache_dir) / "test-package"
    package_dir.mkdir()
    git_url = "https://github.com/user/repo.git"
    
    write_meta_info(package_dir, git_url)
    
    meta_file = package_dir / "meta.json"
    assert meta_file.exists()
    
    with open(meta_file) as f:
        meta = json.load(f)
        assert meta["git_url"] == git_url
        assert "installed_at" in meta
        assert "last_updated" in meta

@pytest.mark.integration
def test_clone_or_pull(temp_cache_dir):
    """Test repository cloning and pulling."""
    git_url = "https://github.com/test/repo.git"
    repo_hash = safe_path(git_url)
    package_dir = os.path.join(temp_cache_dir, repo_hash)
    repo_dir = os.path.join(package_dir, "repo")
    
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        
        # Test initial clone
        result_path = clone_or_pull(git_url)
        assert result_path == repo_dir
        assert os.path.exists(package_dir)
        
        # Verify clone call
        clone_call = mock_run.call_args_list[0]
        assert clone_call == call(
            ['git', 'clone', git_url, repo_dir],
            check=True,
            capture_output=True,
            text=True
        )
        
        # Create the repo directory to simulate existing installation
        os.makedirs(repo_dir, exist_ok=True)
        
        # Test pull on existing repo
        result_path = clone_or_pull(git_url)
        assert result_path == repo_dir
        
        # Verify pull call
        pull_call = mock_run.call_args_list[1]
        assert pull_call == call(
            ['git', 'pull'],
            cwd=repo_dir,
            check=True,
            capture_output=True,
            text=True
        )
        
        # Test force clone
        result_path = clone_or_pull(git_url, force=True)
        assert result_path == repo_dir
        
        # Verify force clone call
        force_clone_call = mock_run.call_args_list[2]
        assert force_clone_call == call(
            ['git', 'clone', git_url, repo_dir],
            check=True,
            capture_output=True,
            text=True
        )

@pytest.mark.integration
def test_clone_or_pull_with_invalid_url(temp_cache_dir):
    """Test error handling for invalid git URLs."""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = Exception("Git error")
        with pytest.raises(Exception):
            clone_or_pull("https://invalid-url/repo.git") 