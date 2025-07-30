from os import environ
from pathlib import Path

from rich import print

from macrostrat.utils import cmd

from .dependencies import get_local_dependencies, load_poetry_config


def install_packages(
    path: Path = Path.cwd(),
    omit: list[str] = [],
    skip_root: bool = False,
    virtualenvs: bool = False,
):
    """Install all packages in the root project's virtual environment."""
    cfg = load_poetry_config(path)
    local_deps = get_local_dependencies(cfg)
    lock_cmd = "poetry lock"

    extra_env = {}
    if not virtualenvs:
        extra_env = {"POETRY_VIRTUALENVS_CREATE": "False"}

    for k, v in local_deps.items():
        _dir = v["path"]
        fp = path / _dir
        cfg = load_poetry_config(path / _dir)
        if k in omit:
            continue
        print(f"Locking dependencies for [bold cyan]{cfg['name']}[/]...")

        cmd(
            lock_cmd,
            cwd=fp,
            env={**environ, **extra_env},
        )
        print()
    if not skip_root:
        print(f"Installing project...")
        cmd(lock_cmd)
        cmd("poetry install")
