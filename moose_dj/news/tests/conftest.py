import subprocess
import sys
import contextlib

import pytest


@pytest.fixture(scope="function")
def long_running_command():
    """
    Starts a long-running Django management command as a background process.

    Yields control to the test while the process is running.
    """

    @contextlib.contextmanager
    def _run_command():
        process = subprocess.Popen(
            [
                sys.executable,
                "manage.py",
                # "run_huey", # Run standard huey ( https://github.com/coleifer/huey )
                "djangohuey", # Run https://github.com/gaiacoop/django-huey
                # "arg1", "arg2"
            ]
        )
        try:
            yield process
        finally:
            # Gracefully terminate the process
            process.terminate()
            process.wait()

    with _run_command() as process:
        yield process
