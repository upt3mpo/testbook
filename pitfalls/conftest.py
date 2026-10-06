"""Shared fixtures for the Python-track pitfall tests.

Mirrors fixtures.js: ONE test body runs against both the broken and the fixed page. On the
broken page the reference test is expected to fail (strict xfail), which is what proves the
pitfall is real. Pass --show-red (or set SHOW_RED=1) to see the real failure instead.
"""

import os
import socket
import subprocess
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).parent
PORT = int(os.getenv("PITFALLS_PORT", "4100"))
BASE_URL = f"http://localhost:{PORT}"


def pytest_addoption(parser):
    parser.addoption("--show-red", action="store_true", help="Do not mark broken-page failures as expected")
    parser.addoption("--exercises", action="store_true", help="Also collect learner exercise files")


def pytest_ignore_collect(collection_path, config):
    # Learner skeletons are skipped unless asked for, so the reference suite stays green.
    if "exercise" in collection_path.parts and not config.getoption("--exercises"):
        return True
    return None


def _port_open() -> bool:
    with socket.socket() as s:
        s.settimeout(0.3)
        return s.connect_ex(("127.0.0.1", PORT)) == 0


@pytest.fixture(scope="session", autouse=True)
def pitfalls_server():
    """Start the static server (node serve.mjs) unless one is already running."""
    if _port_open():
        yield
        return
    proc = subprocess.Popen(["node", "serve.mjs"], cwd=ROOT, stdout=subprocess.DEVNULL)
    for _ in range(50):
        if _port_open():
            break
        time.sleep(0.1)
    yield
    proc.terminate()


@pytest.fixture(params=["broken", "fixed"])
def variant(request):
    return request.param


@pytest.fixture
def open_pitfall(page, variant):
    def _open(directory: str):
        page.goto(f"{BASE_URL}/{directory}/{variant}/")

    return _open


@pytest.fixture
def expect_bug_on_broken(request, variant):
    """Call as expect_bug_on_broken("why") at the top of a test."""

    def _mark(reason: str):
        show_red = request.config.getoption("--show-red") or os.getenv("SHOW_RED")
        if variant == "broken" and not show_red:
            request.applymarker(pytest.mark.xfail(strict=True, reason=reason))

    return _mark


@pytest.fixture(scope="session")
def axe_source():
    """The axe-core script, injected into pages by Python tests (no Python axe wrapper needed)."""
    path = ROOT / "node_modules" / "axe-core" / "axe.min.js"
    if not path.exists():
        pytest.skip("Run `npm install` in pitfalls/ first: Python tests inject axe-core from node_modules")
    return path.read_text(encoding="utf-8")
