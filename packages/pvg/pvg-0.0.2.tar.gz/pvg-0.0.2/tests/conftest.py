import os
import shutil
import tempfile
import pytest
from pathlib import Path
from unittest.mock import patch

@pytest.fixture
def temp_cache_dir():
    """Create a temporary directory for cache testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        old_cache_dir = os.environ.get('PVG_CACHE_DIR')
        os.environ['PVG_CACHE_DIR'] = temp_dir
        yield temp_dir
        if old_cache_dir:
            os.environ['PVG_CACHE_DIR'] = old_cache_dir
        else:
            del os.environ['PVG_CACHE_DIR']

@pytest.fixture
def mock_git_repo():
    """Create a temporary git repository for testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        repo_dir = Path(temp_dir)
        
        # Mock git commands instead of actually running them
        with patch('subprocess.run') as mock_run:
            mock_run.return_value.returncode = 0
            
            # Create a simple Python package
            setup_py = repo_dir / 'setup.py'
            setup_py.write_text('''
from setuptools import setup
setup(
    name="test-package",
    version="0.1.0",
)
''')
            
            # Create an empty package
            pkg_dir = repo_dir / 'test_package'
            pkg_dir.mkdir()
            (pkg_dir / '__init__.py').touch()
            
            yield repo_dir 