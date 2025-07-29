# PVG - pip-via-git

A command-line tool for installing Python packages directly from Git repositories.

## Installation

To install the tool for development:

```bash
pip install -e .
```

## Requirements

- Git must be installed and accessible from the command line
- Python 3.8 or higher
- pip
- SSH key configured with GitHub (if using SSH URLs)

## Usage

There are several ways to install packages:

### Using GitHub repository names

Install a package from GitHub using HTTPS (default):
```bash
pvg install username/repository
```

Install a package using SSH:
```bash
pvg install --use-ssh username/repository
```

Force a fresh clone (deleting cached version if it exists):
```bash
pvg install --force username/repository
```

### Using direct Git URLs

You can also use any Git URL directly:

```bash
# Using HTTPS URL
pvg install https://github.com/username/repository.git

# Using SSH URL
pvg install git@github.com:username/repository.git

# Using other Git URLs
pvg install https://gitlab.com/username/repository.git
pvg install git://git.example.com/repository.git
```

### Managing the Cache

List all cached repositories and their metadata:
```bash
pvg list-cache
```

Clean all cached repositories:
```bash
pvg clean-cache
```

## Examples

Install Click from GitHub using repository name:
```bash
pvg install pallets/click
```

Install Click using direct HTTPS URL with force flag:
```bash
pvg install --force https://github.com/pallets/click.git
```

## How it works

The `install` command:
1. Accepts either a GitHub repository name or a complete Git URL
2. For GitHub repository names:
   - Converts them to HTTPS or SSH URLs based on the `--use-ssh` flag
3. For Git URLs:
   - Uses the URL as-is without modification
4. Manages the repository in the cache (`~/.pvg-cache/`):
   - Creates a unique directory based on the URL's hash
   - Stores metadata in `meta.json`
   - Clones the repository into the `repo` subdirectory
   - If it exists: Pulls latest changes (unless `--force` is used)
   - If `--force` is used: Deletes and clones fresh
5. Runs `pip install -e .` in the cached repository

## Commands

- `pvg install [OPTIONS] <package>`: Install a Python package from a Git repository
  - `<package>`: Can be either a GitHub repository name (e.g., `username/repository`) or a complete Git URL
  - `--use-ssh`: Optional flag to use SSH URL instead of HTTPS when using GitHub repository names
  - `--force`: Optional flag to force delete and clone the repository even if it exists in cache
- `pvg list-cache`: List all cached repositories and their metadata
- `pvg clean-cache`: Clean the package cache directory (`~/.pvg-cache`)

## Cache Directory Structure

The cache is organized in `~/.pvg-cache/` as follows:

```
~/.pvg-cache/
├── <url-hash-1>/
│   ├── meta.json    # Contains git URL and timestamps
│   └── repo/        # The actual git repository
├── <url-hash-2>/
│   ├── meta.json
│   └── repo/
└── ...
```

The cache can be:
- Updated automatically when installing (git pull)
- Inspected using the `list-cache` command
- Cleaned manually using the `clean-cache` command
- Bypassed using the `--force` flag during installation
