"""Let scheduled runs catch up when the live puzzle has the wrong UTC date."""

import argparse
import os
import sys
import time
from datetime import date, datetime, timezone
from http.client import HTTPException
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urljoin
from urllib.request import Request, urlopen

from verify_deployment import mystery_date


def needs_generation(site_url, today=None, attempts=3, interval=10):
    today = today or datetime.now(timezone.utc).date()
    data_url = urljoin(site_url.rstrip("/") + "/", "data.js")
    for attempt in range(1, attempts + 1):
        request = Request(
            data_url + "?mystery-update-check=" + str(time.time_ns()),
            headers={"Cache-Control": "no-cache, no-store", "Pragma": "no-cache"},
        )
        try:
            with urlopen(request, timeout=10) as response:
                live_date = date.fromisoformat(mystery_date(response.read()))
            generate = live_date != today
            print("Live puzzle: {}; expected UTC date: {}. {}".format(
                live_date, today,
                "Generation required." if generate else "Today's puzzle is already live; skipping generation.",
            ), flush=True)
            return generate
        except (URLError, OSError, HTTPException, ValueError) as error:
            print("Check {}/{} failed: {}".format(attempt, attempts, error), flush=True)
            if attempt < attempts:
                time.sleep(interval)
    print("Unable to confirm today's puzzle after retries; generation required.", flush=True)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site-url", default="https://mystery-o-matic.com/")
    parser.add_argument("--date", type=date.fromisoformat, dest="today")
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--interval", type=float, default=10)
    args = parser.parse_args()
    if args.attempts < 1 or args.interval < 0:
        parser.error("attempts must be positive and interval must be nonnegative")
    generate = needs_generation(**vars(args))
    output = "generate={}\n".format(str(generate).lower())
    if os.environ.get("GITHUB_OUTPUT"):
        with Path(os.environ["GITHUB_OUTPUT"]).open("a") as target:
            target.write(output)
    print(output, end="")
    return 0


if __name__ == "__main__":
    sys.exit(main())
