from invoke.context import Context
from invoke.tasks import task

from tasks.common import VENV_PREFIX


@task
def commit(ctx: Context, pty: bool = True) -> None:
    """Commit through commitizen"""
    ctx.run(f"{VENV_PREFIX} cz commit", pty=pty)


@task
def bump(ctx: Context, changelog: bool = False) -> None:
    """Bump version through commitizen"""
    arguments: str = " --changelog" if changelog else ""

    ctx.run(f"{VENV_PREFIX} cz bump -nr 3 --yes{arguments}", warn=True)
