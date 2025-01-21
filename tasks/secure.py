from invoke.context import Context
from invoke.tasks import task

from tasks.common import VENV_PREFIX


@task
def check_package(ctx: Context, pty: bool = True) -> None:
    """Check package security"""
    ctx.run(f"{VENV_PREFIX} pip-audit", warn=True, pty=pty)


@task
def bandit(ctx: Context, pty: bool = True) -> None:
    """Check common software vulnerabilities (Use it as reference only)"""
    ctx.run(f"{VENV_PREFIX} bandit -r -iii -lll --ini .bandit", pty=pty)


@task(default=True)
def run(ctx: Context, pty: bool = True) -> None:
    """Check security check through pip-audit and bandit"""
    # switch this from pre-executes to enable passing the pty parameter
    check_package(ctx, pty=pty)
    bandit(ctx, pty=pty)
    pass
