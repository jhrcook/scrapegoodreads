"""Webscraping data from Goodreads."""

from typing import Final

__version__ = "0.0.0.9000"

GOODREADS_BASE_URL: Final[str] = "https://www.goodreads.com"

GOODREADS_URLS: Final[dict[str, str]] = {
    "user": "https://www.goodreads.com/user/show/",
    "list": GOODREADS_BASE_URL + "/review/list/",
}
