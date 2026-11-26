import os
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "check_daily_mystery.py"


@pytest.fixture
def server():
    responses = []
    requests = []

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            requests.append((self.path, self.headers))
            status, body = responses.pop(0)
            self.send_response(status)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def log_message(self, *args):
            pass

    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=httpd.serve_forever, daemon=True)
    worker.start()
    try:
        yield "http://127.0.0.1:{}".format(httpd.server_port), responses, requests
    finally:
        httpd.shutdown()
        httpd.server_close()
        worker.join()


@pytest.mark.parametrize("live_date,expected", [
    ("2026-11-26", "false"),
    ("2026-11-25", "true"),
    ("2026-11-27", "true"),
])
def test_checks_requested_utc_day_and_writes_workflow_output(server, tmp_path, live_date, expected):
    url, responses, requests = server
    responses.append((200, ('data = {"mysteryDate": "%s"};' % live_date).encode()))
    output = tmp_path / "output"
    output.write_text("previous=value\n")
    result = subprocess.run([
        sys.executable, str(SCRIPT), "--site-url", url, "--date", "2026-11-26",
    ], env={**os.environ, "GITHUB_OUTPUT": str(output)}, capture_output=True, text=True)
    assert result.returncode == 0
    assert output.read_text() == "previous=value\ngenerate=" + expected + "\n"
    assert len(requests) == 1
    assert requests[0][0].startswith("/data.js?mystery-update-check=")
    assert "no-cache" in requests[0][1]["Cache-Control"]


@pytest.mark.parametrize("failure", [(503, b"unavailable"), (200, b"not puzzle data")])
def test_transient_read_failure_does_not_regenerate_a_current_puzzle(server, tmp_path, failure):
    url, responses, requests = server
    responses.extend([failure, (200, b'data = {"mysteryDate": "2026-11-26"}')])
    output = tmp_path / "output"
    result = subprocess.run([
        sys.executable, str(SCRIPT), "--site-url", url, "--date", "2026-11-26",
        "--attempts", "2", "--interval", "0",
    ], env={**os.environ, "GITHUB_OUTPUT": str(output)}, capture_output=True, text=True)
    assert result.returncode == 0
    assert output.read_text() == "generate=false\n"
    assert len(requests) == 2
    assert requests[0][0] != requests[1][0]


def test_persistent_read_failure_requests_generation_after_bounded_retries(server, tmp_path):
    url, responses, requests = server
    responses.extend([(503, b"unavailable")] * 3)
    output = tmp_path / "output"
    result = subprocess.run([
        sys.executable, str(SCRIPT), "--site-url", url, "--date", "2026-11-26",
        "--attempts", "3", "--interval", "0",
    ], env={**os.environ, "GITHUB_OUTPUT": str(output)}, capture_output=True, text=True)
    assert result.returncode == 0
    assert output.read_text() == "generate=true\n"
    assert len(requests) == 3
