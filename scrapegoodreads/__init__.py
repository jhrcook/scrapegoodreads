"""Webscraping data from Goodreads."""

import logging
from typing import Final

__version__: Final[str] = "0.0.0.9000"

logging.basicConfig()
logger = logging.getLogger(__name__)

GOODREADS_BASE_URL: Final[str] = "https://www.goodreads.com"

GOODREADS_URLS: Final[dict[str, str]] = {
    "user": GOODREADS_BASE_URL + "/user/show/",
    "list": GOODREADS_BASE_URL + "/review/list/",
    "sign-in": GOODREADS_BASE_URL + "/user/sign_in",
}
