import subprocess
import sys
import contextlib
from pathlib import Path
from threading import Thread
from fakeredis import FakeStrictRedis, TcpFakeServer
from time import sleep
import docker
from contextlib import contextmanager
from docker.errors import DockerException

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
                "djangohuey",  # Run https://github.com/gaiacoop/django-huey
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

        server = TcpFakeServer(server_address, server_type="valkey")
        # thread = Thread(target=server.serve_forever, daemon=True)
        # thread.start()

        fsr_server = FakeStrictRedis(server=server, singleton=True)

        try:
            yield fsr_server
        except:
            # thread.join()
            server.shutdown()
        finally:
            # Gracefully terminate the thread
            # thread.kill()
            # thread.join()
            server.shutdown()

    with _run_command() as process:
        yield process


@pytest.fixture(scope="function")
def celery_worker_fixture(redis_container):
    """
    Starts a long-running Django management command as a background process.

    Yields control to the test while the process is running.
    """

    @contextlib.contextmanager
    def _run_command():
        process = subprocess.Popen(
            [sys.executable, "-m", "celery", "-A", "moose_dj", "worker"]
        )
        try:
            yield process
        finally:
            # Gracefully terminate the process
            process.terminate()
            process.wait()

    with _run_command() as process:
        yield process


@pytest.fixture(scope="function")
def redis_container():
    """
    Context manager to launch a Redis container named 'my-redis' on localhost:6379.
    Deletes the container if it already exists or when the context exits.
    """
    client = None
    container = None
    try:
        client = docker.from_env()
    except DockerException as e:
        print("DockerException:", e)
        home = Path.home()
        socket = f"unix:///{home}/.colima/default/docker.sock"
        client = docker.DockerClient(base_url=socket)

    if client is None:
        raise Exception("Could not create Docker client")

    try:
        # Check if the container already exists
        try:
            existing_container = client.containers.get("my-redis")
            existing_container.stop()
            existing_container.remove()
        except docker.errors.NotFound:
            pass

        # Create and start the container
        container = client.containers.run(
            # "redis"
            "redis:6",
            detach=True,
            name="my-redis",
            ports={"6379/tcp": 6379},
        )

        logs = container.logs(stream=True)
        for log in logs:
            if b"Ready to accept connections" in log:
                break

        yield container

    finally:
        # Remove the container on exit
        try:
            container.remove(force=True)
        except docker.errors.NotFound:
            pass
