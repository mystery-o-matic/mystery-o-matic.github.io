import importlib.util
import subprocess
import sys
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from unittest.mock import patch
from urllib.error import URLError

import pytest


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "verify_deployment.py"
spec = importlib.util.spec_from_file_location("verify_deployment", SCRIPT)
deployment = importlib.util.module_from_spec(spec)
spec.loader.exec_module(deployment)

CURRENT = b'data = {"mysteryDate": "2026-11-24", "puzzle": "current"}'
OLD = b'data = {"mysteryDate": "2026-11-23", "puzzle": "old"}'


@pytest.fixture
def expected_file(tmp_path):
    path = tmp_path / "data.js"
    path.write_bytes(CURRENT)
    return path


@pytest.fixture
def live_server():
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

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    worker = threading.Thread(target=server.serve_forever, daemon=True)
    worker.start()
    try:
        yield "http://127.0.0.1:{}".format(server.server_port), responses, requests
    finally:
        server.shutdown()
        server.server_close()
        worker.join()


def test_retries_stale_puzzle_until_exact_artifact_is_live(expected_file, live_server):
    url, responses, requests = live_server
    responses.extend([(200, OLD), (200, CURRENT)])
    with patch.object(deployment.time, "sleep") as sleep:
        assert deployment.verify_deployment(expected_file, url, attempts=3, interval=30)
    sleep.assert_called_once_with(30)
    assert len(requests) == 2
    assert requests[0][0] != requests[1][0]
    for path, headers in requests:
        assert path.startswith("/data.js?mystery-update-check=")
        assert "no-cache" in headers["Cache-Control"]


@pytest.mark.parametrize("body", [OLD, CURRENT.replace(b"current", b"different"), b"<html>Error</html>"])
def test_cli_fails_if_live_data_never_matches(expected_file, live_server, body):
    url, responses, requests = live_server
    responses.extend([(200, body), (200, body)])
    result = subprocess.run([
        sys.executable, str(SCRIPT), str(expected_file), "--site-url", url,
        "--attempts", "2", "--interval", "0",
    ], capture_output=True, text=True)
    assert result.returncode == 1
    assert "Deployment verification failed" in result.stderr
    assert len(requests) == 2


def test_retries_transient_http_error(expected_file, live_server):
    url, responses, requests = live_server
    responses.extend([(503, b"unavailable"), (200, CURRENT)])
    assert deployment.verify_deployment(expected_file, url + "/", attempts=2, interval=0)
    assert len(requests) == 2


def test_cli_succeeds_for_exact_artifact_on_project_site(expected_file, live_server):
    url, responses, requests = live_server
    responses.append((200, CURRENT))
    result = subprocess.run([
        sys.executable, str(SCRIPT), str(expected_file), "--site-url", url + "/project/",
        "--attempts", "1",
    ], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Verified live puzzle 2026-11-24" in result.stdout
    assert requests[0][0].startswith("/project/data.js?")


def test_network_failure_exhausts_retries_without_sleeping_after_last_attempt(expected_file):
    with patch.object(deployment, "urlopen", side_effect=URLError("offline")) as fetch:
        with patch.object(deployment.time, "sleep") as sleep:
            assert not deployment.verify_deployment(expected_file, "https://example.com/", attempts=2)
    assert fetch.call_count == 2
    sleep.assert_called_once_with(30)


@pytest.mark.parametrize("contents", [b"not puzzle data", b"data = {}", b"data = null"])
def test_rejects_invalid_expected_artifact_before_fetching(expected_file, contents):
    expected_file.write_bytes(contents)
    with patch.object(deployment, "urlopen") as fetch:
        with pytest.raises(ValueError):
            deployment.verify_deployment(expected_file, "https://example.com/")
    fetch.assert_not_called()
