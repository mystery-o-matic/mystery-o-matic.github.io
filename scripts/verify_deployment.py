"""Fail a deployment when Pages keeps serving a different puzzle artifact."""

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlencode, urljoin, urlsplit
from urllib.request import Request, urlopen


def mystery_date(source):
    match = re.fullmatch(rb"\s*data\s*=\s*([\s\S]*?)\s*;?\s*", source)
    if not match:
        raise ValueError("Expected a data.js file containing a JSON data assignment")
    data = json.loads(match.group(1))
    if not isinstance(data, dict) or not isinstance(data.get("mysteryDate"), str):
        raise ValueError("Puzzle data is missing mysteryDate")
    return data["mysteryDate"]


def verify_deployment(data_path, site_url, attempts=25, interval=30, request_timeout=10):
    if attempts < 1 or interval < 0 or request_timeout <= 0:
        raise ValueError("Use positive attempts and request timeout, and a nonnegative interval")
    if urlsplit(site_url).scheme not in ("http", "https") or not urlsplit(site_url).netloc:
        raise ValueError("The site URL must be an absolute HTTP or HTTPS URL")

    expected = Path(data_path).read_bytes()
    expected_date = mystery_date(expected)
    expected_hash = hashlib.sha256(expected).hexdigest()
    data_url = urljoin(site_url.rstrip("/") + "/", "data.js")
    print("Expected puzzle: {} (SHA-256 {})".format(expected_date, expected_hash), flush=True)

    for attempt in range(1, attempts + 1):
        query = urlencode({"mystery-update-check": time.time_ns()})
        request = Request(data_url + "?" + query, headers={
            "Cache-Control": "no-cache, no-store",
            "Pragma": "no-cache",
            "User-Agent": "mystery-o-matic-deployment-check",
        })
        try:
            with urlopen(request, timeout=request_timeout) as response:
                actual = response.read()
                last_modified = response.headers.get("Last-Modified", "unknown")
            if actual == expected:
                print("Verified live puzzle {} at {}".format(expected_date, data_url), flush=True)
                return True
            try:
                actual_date = mystery_date(actual)
            except (ValueError, UnicodeError):
                actual_date = "unreadable"
            detail = "received {} (SHA-256 {}, Last-Modified {})".format(
                actual_date, hashlib.sha256(actual).hexdigest(), last_modified
            )
        except (URLError, OSError) as error:
            detail = "request failed: {}".format(error)
        print("Attempt {}/{}: {}".format(attempt, attempts, detail), flush=True)
        if attempt < attempts:
            time.sleep(interval)

    print(
        "Deployment verification failed: {} does not match the uploaded puzzle. "
        "Republish the saved github-pages artifact using the Republish saved mystery workflow.".format(data_url),
        file=sys.stderr,
        flush=True,
    )
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data_path", type=Path, help="Generated data.js to compare with the live site")
    parser.add_argument("--site-url", required=True, help="Published site root URL")
    parser.add_argument("--attempts", type=int, default=25)
    parser.add_argument("--interval", type=float, default=30)
    parser.add_argument("--request-timeout", type=float, default=10)
    args = parser.parse_args()
    try:
        verified = verify_deployment(**vars(args))
    except (OSError, ValueError) as error:
        parser.error(str(error))
    return 0 if verified else 1


if __name__ == "__main__":
    sys.exit(main())
