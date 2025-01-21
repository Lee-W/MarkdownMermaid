from invoke.context import Context
from invoke.tasks import task

from tasks.common import VENV_PREFIX


@task(default=True)
def run(ctx: Context, allow_no_tests: bool = False, pty: bool = True) -> None:
    """Run test cases"""
    result = ctx.run(f"{VENV_PREFIX} pytest", pty=pty, warn=True)
    if allow_no_tests and result.exited == 5:
        exit(0)
    exit(result.exited)


@task
def cov(ctx: Context, pty: bool = True) -> None:
    """Run test coverage check"""
    ctx.run(f"{VENV_PREFIX} pytest --cov=markdown_mermaidjs tests/", pty=pty)
