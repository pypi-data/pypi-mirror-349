from dataclasses import dataclass

import click
import os
import subprocess
import tempfile
import shutil
from pathlib import Path
import re
import hashlib
import json


def is_git_url(url):
    """Check if the input is a git URL."""
    git_url_patterns = [
        r'^https?://.*\.git$',
        r'^git@.*:.*\.git$',
        r'^git://.*\.git$',
        r'^ssh://.*\.git$'
    ]
    return any(re.match(pattern, url) for pattern in git_url_patterns)


def get_cache_dir():
    """Get the cache directory path.

    The cache directory can be configured using the PVG_CACHE_DIR environment variable.
    If not set, defaults to ~/.pvg-cache/
    """
    return os.environ.get('PVG_CACHE_DIR') or os.path.expanduser("~/.pvg-cache")


def safe_path(url):
    """Convert a URL to a safe directory name using SHA-256."""
    return hashlib.sha256(url.encode()).hexdigest()


def ensure_cache_dir():
    """Ensure the cache directory exists."""
    cache_dir = get_cache_dir()
    os.makedirs(cache_dir, exist_ok=True)
    return cache_dir


def write_meta_info(package_dir, git_url):
    """Write metadata information to meta.json."""
    meta_file = os.path.join(package_dir, "meta.json")
    meta_info = {
        "git_url": git_url,
        "installed_at": str(Path(package_dir).stat().st_mtime),
        "last_updated": str(Path(package_dir).stat().st_mtime)
    }
    with open(meta_file, "w") as f:
        json.dump(meta_info, f, indent=2)


def clone_or_pull(git_url, force=False):
    """Clone a new repository or pull if it exists."""
    cache_dir = ensure_cache_dir()
    package_dir = os.path.join(cache_dir, safe_path(git_url))
    repo_dir = os.path.join(package_dir, "repo")

    if os.path.exists(repo_dir):
        if force:
            click.echo("Force flag used. Removing existing repository...")
            shutil.rmtree(package_dir)
        else:
            click.echo(f"Repository cache exists at {repo_dir}")
            click.echo("Pulling latest changes...")
            try:
                subprocess.run(
                    ["git", "pull"],
                    cwd=repo_dir,
                    check=True,
                    capture_output=True,
                    text=True
                )
                # Update last_updated in meta.json
                write_meta_info(package_dir, git_url)
                return repo_dir
            except subprocess.CalledProcessError as e:
                click.echo(f"Pull failed: {e.stderr}", err=True)
                if click.confirm("Would you like to force delete and clone again?"):
                    shutil.rmtree(package_dir)
                else:
                    raise click.Abort()

    # Clone if directory doesn't exist or was deleted
    if not os.path.exists(repo_dir):
        os.makedirs(package_dir, exist_ok=True)
        click.echo(f"Cloning repository to {repo_dir}")
        subprocess.run(
            ["git", "clone", git_url, repo_dir],
            check=True,
            capture_output=True,
            text=True
        )
        # Write initial meta.json
        write_meta_info(package_dir, git_url)

    return repo_dir


def install_package(git_url, force=False):
    repo_path = clone_or_pull(git_url, force)

    click.echo(f"Installing package from {repo_path}")
    # Run pip install -e in the cloned repository
    result = subprocess.run(
        ["pip", "install", "-e", "."],
        cwd=repo_path,
        check=True,
        capture_output=True,
        text=True
    )
    if result.stdout:
        click.echo("Output:")
        click.echo(result.stdout)
    if result.stderr:
        click.echo("Errors:")
        click.echo(result.stderr)


@dataclass
class InstallTarget:
    is_url: bool
    url: str = None
    package: str = None
    use_ssh: bool = False

    def __repr__(self):
        if self.is_url:
            return self.url
        else:
            if self.use_ssh:
                return self.package
            else:
                return f"ssh:{self.package}"


def parse_line(line) -> InstallTarget:
    """
    Parse a package definition line in one of the following formats:
        * `ssh:user/repo_name`: InstallTarget(is_url=False, package="user/repo_name", use_ssh=True)
        * `user/repo_name`: InstallTarget(is_url=False, package="user/repo_name", use_ssh=False)
        * raw_full_url: InstallTarget(is_url=True, url=url)

    Args:
        line (str): The line to parse

    Returns:
        InstallTarget: Parsed installation target

    Raises:
        ValueError: If the line format is invalid
    """
    # Strip whitespace
    line = line.strip()

    # Check if it's a raw URL
    if is_git_url(line):
        return InstallTarget(is_url=True, url=line)

    # Check if it's an SSH format
    if line.startswith('ssh:'):
        package = line[4:]  # Remove 'ssh:' prefix
        if '/' not in package:
            raise ValueError(f"Invalid ssh format. Expected 'ssh:user/repo', got '{line}'")
        return InstallTarget(is_url=False, package=package, use_ssh=True)

    # Default case: validate user/repo format
    if not line or '/' not in line or line.count('/') > 1:
        raise ValueError(f"Invalid format. Expected 'user/repo', got '{line}'")

    # Verify there's content before and after the slash
    user, repo = line.split('/')
    if not user or not repo:
        raise ValueError(f"Invalid format. User and repo name cannot be empty in '{line}'")

    return InstallTarget(is_url=False, package=line, use_ssh=False)


def resolve_git_url(package, use_ssh):
    if is_git_url(package):
        git_url = package
        click.echo(f"Using provided git URL: {git_url}")
    else:
        # Convert package name to git URL based on protocol choice
        if use_ssh:
            git_url = f"git@github.com:{package}.git"
        else:
            git_url = f"https://github.com/{package}.git"
        click.echo(f"Using {'SSH' if use_ssh else 'HTTPS'} GitHub URL: {git_url}")


def install_all(fp: str, force: bool = False):
    targets = []
    with open(fp, "r") as f:
        for line in f:
            targets.append(parse_line(line.strip()))
    for t in targets:
        click.echo(f'installing {t.url if t.is_url else t.package}')
        install_package(resolve_git_url(t.package, t.use_ssh), force=force)


def strip_comment(line: str) -> str:
    """
    Removes comments and leading/trailing whitespace from a line of text.
    A comment starts with the '#' character. Lines that are empty or consist
    entirely of comments are returned as an empty string.

    Args:
        line (str): A single line of text.

    Returns:
        str: The line with any comments removed, or an empty string if the line
             is blank or a full-line comment.
    """
    if not line:
        return ""

    # Remove inline comments and strip leading/trailing whitespace
    line = line.split("#", 1)[0].strip()

    return line


def add_dependency_to_file(fp: str, package: str, use_ssh: bool = False):
    existing_targets = []
    with open(fp, "r") as f:
        for line in f:
            line = strip_comment(line)
            if len(line) == 0:
                continue
            existing_targets.append(line)

    if package in existing_targets:
        return
    else:
        with open(fp, "a") as f:
            if is_git_url(package):
                f.write(f"{package}\n")
                return
            else:
                if use_ssh:
                    f.write(f"ssh:{package}\n")
                else:
                    f.write(f"{package}\n")
