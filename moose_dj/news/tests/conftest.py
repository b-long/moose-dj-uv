import subprocess
import sys
import contextlib
import fakeredis
from threading import Thread
from fakeredis import TcpFakeServer

import pytest

@pytest.fixture(scope="function")
def huey_worker_fixture():
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


@pytest.fixture()
def fake_redis_fixture():

    @contextlib.contextmanager
    def _run_command():
        server_address = ("127.0.0.1", 6379)
        server = TcpFakeServer(server_address, server_type="redis")
        thread = Thread(target=server.serve_forever, daemon=True)
        thread.start()


        try:
            yield thread
        finally:
            # Gracefully terminate the thread
            # thread.stop()
            thread.join()


    with _run_command() as process:
        yield process


@pytest.fixture(scope="function")
def celery_worker_fixture(fake_redis_fixture):
    """
    Starts a long-running Django management command as a background process.

    Yields control to the test while the process is running.
    """

    @contextlib.contextmanager
    def _run_command():
        process = subprocess.Popen(
            [
                sys.executable,
                "-m",
                "celery",
                "-A",
                "moose_dj",
                "worker"
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
