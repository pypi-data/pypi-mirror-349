"""
This module houses utility functions that are shared between Sparrow's
core and command-line interface.
"""
import os
from contextlib import contextmanager
from pathlib import Path

from .exc import ApplicationError, BaseError
from .logs import get_logger, setup_stderr_logs
from .shell import cmd, split_args
from .timer import CodeTimer


def relative_path(base, *parts) -> Path:
    if not os.path.isdir(str(base)):
        base = os.path.dirname(base)
    return Path(os.path.join(base, *parts))


@contextmanager
def working_directory(path: Path):
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    """
    prev_cwd = os.getcwd()
    os.chdir(str(path))
    yield
    os.chdir(prev_cwd)


@contextmanager
def override_environment(**kwargs):
    """Override environment variables for a block of code."""
    old_environ = dict(os.environ)
    os.environ.update(kwargs)
    try:
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_environ)
