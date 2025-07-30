from datetime import UTC, datetime
from typing import Any

from click.exceptions import Exit
from mm_std import Result, fatal, print_json


def print_debug_or_error(res: Result[Any], debug: bool) -> None:
    if debug:
        print_json(res)
        raise Exit

    if res.is_err():
        fatal(res.unwrap_error())


def format_ts(ts: int) -> str:
    return datetime.fromtimestamp(ts / 1000, tz=UTC).strftime("%Y-%m-%d %H:%M:%S")
