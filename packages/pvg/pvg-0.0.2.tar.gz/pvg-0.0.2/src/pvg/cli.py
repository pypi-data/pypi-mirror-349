import collections
import json
import os
import shutil
import subprocess

import click

from pvg.core import is_git_url, clone_or_pull, get_cache_dir, install_all, add_dependency_to_file


class OrderedGroup(click.Group):
    def __init__(self, name=None, commands=None, **attrs):
        super(OrderedGroup, self).__init__(name, commands, **attrs)
        #: the registered subcommands by their exported names.
        self.commands = commands or collections.OrderedDict()

    def list_commands(self, ctx):
        return self.commands


@click.group(cls=OrderedGroup)
def cli():
    """PVG - pip-via-git: Install Python packages directly from Git repositories."""
    pass


DEFAULT_REQ_FILE = 'pvg-requirements.txt'


@cli.command(name='init')
@click.option('--file', '-f', help='dependencies file path', default=DEFAULT_REQ_FILE)
def init_cmd(file):
    """
    create a pvg-requirements.txt file.
    :param file:
    :return:
    """
    if os.path.exists(file):
        click.echo(f"File '{file}' already exists. Skipping initialization.")
        return
    else:
        with open(file, 'w') as f:
            f.write(
                "# Add your dependencies here.\n"
                "# Each line should be in the format: \n"
                "# user/repo_name # github repo \n"
                "# ssh:user/repo_name # github repo using ssh\n"
                "# https://github.com/username/repo.git # any git repo url\n"
                '# git@.*:.*\.git # any git repo \n'
                '# git://.*\.git # any git repo \n'
                '# ssh://.*\.git # any git repo \n'

            )

        click.echo(f"Created '{file}'.")


@cli.command(name='add')
@click.argument('package')
@click.option('--file', '-f', help='dependencies file path', default=DEFAULT_REQ_FILE)
@click.option('--use-ssh', is_flag=True, default=False, help='Use SSH URL instead of HTTPS for git clone')
@click.option('--force', is_flag=True, default=False,
              help='Force delete and clone the repository even if it exists in cache')
@click.option('--do-not-add', '-d', 'do_not_add', is_flag=True, default=False,
              help='Skip adding this package to the dependencies file.')
def add_cmd(package, file, use_ssh, force, do_not_add):
    """Install a package from the specified source.
    
    Example: pvg install hello/world
            pvg install https://github.com/username/repo.git
            pvg install git@github.com:username/repo.git
    
    This will clone the git repository and install the package using pip.
    The repository can be cloned using either HTTPS (default) or SSH URLs.
    For GitHub repositories, you can specify either the repository name or the full URL.
    Repositories are cached in ~/.pvg-cache/ and updated using git pull unless --force is used.
    """
    # Determine if the package is a URL or a GitHub repository name
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

    try:
        # Clone or pull the repository
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

        if not do_not_add:
            add_dependency_to_file(file, package, use_ssh)

        click.echo("Installation successful!")

    except subprocess.CalledProcessError as e:
        click.echo(f"Error: {e.stderr}", err=True)
        raise click.Abort()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)
        raise click.Abort()


@cli.command('install',
             help='Install all packages from a file.')
@click.option('--file', '-f', help='dependencies file path', default=DEFAULT_REQ_FILE)
@click.option('--force', is_flag=True, default=False,
              help='Force delete and clone the repository even if it exists in cache')
def install_all_cmd(file, force):
    """Install all packages from a file."""
    install_all(file, force)


@cli.group()
def cache():
    """Cache management commands."""
    pass


@cache.command(name="clean")
def clean_cache():
    """Clean the package cache directory (~/.pvg-cache)."""
    cache_dir = get_cache_dir()
    if os.path.exists(cache_dir):
        if click.confirm(f"Are you sure you want to delete all cached repositories in {cache_dir}?"):
            shutil.rmtree(cache_dir)
            click.echo("Cache cleaned successfully!")
        else:
            click.echo("Cache cleaning cancelled.")
    else:
        click.echo("Cache directory doesn't exist.")


@cache.command(name="list")
def list_cache():
    """List all cached repositories and their metadata."""
    cache_dir = get_cache_dir()
    if not os.path.exists(cache_dir):
        click.echo("Cache directory doesn't exist.")
        return

    for package_hash in os.listdir(cache_dir):
        package_dir = os.path.join(cache_dir, package_hash)
        meta_file = os.path.join(package_dir, "meta.json")
        if os.path.exists(meta_file):
            with open(meta_file) as f:
                meta = json.load(f)
                click.echo(f"\nPackage: {meta['git_url']}")
                click.echo(f"Cache location: {package_dir}")
                click.echo(f"Last updated: {meta['last_updated']}")


if __name__ == '__main__':
    cli()
