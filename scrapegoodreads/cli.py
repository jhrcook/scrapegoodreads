"""Scrapegoodreads main entrypoint."""

import logging
from pathlib import Path
from typing import Optional

import typer

from scrapegoodreads import GOODREADS_BASE_URL, logger
from scrapegoodreads.configuration import (
    Configuration,
    find_configuration_file,
    read_config,
)
from scrapegoodreads.webscraping_helpers import BuiltinWebDriver, make_builtin_driver

# --- CLI setup ---


app = typer.Typer()
logger.setLevel(logging.INFO)


# --- Utilities ---


class InputException(BaseException):
    """Input exception."""

    ...


def _default_web_driver() -> BuiltinWebDriver:
    return BuiltinWebDriver.BRAVE


# --- Profile ---


@app.command()
def profile(
    config: Optional[Path] = None,
    id: Optional[str] = None,
    driver: Optional[BuiltinWebDriver] = None,
) -> None:
    config = config if config is not None else find_configuration_file()
    gr_config: Configuration
    if config is not None:
        gr_config = read_config(config)
    elif id is not None:
        gr_config = Configuration(user_id=id, driver=driver)
    else:
        raise InputException("Must supply either a configuration file or user ID.")

    if gr_config.driver is None:
        gr_config.driver = _default_web_driver()
        logger.info(f"Using default web driver '{gr_config.driver.value}'")

    web_driver = make_builtin_driver(gr_config.driver)
    web_driver.get(GOODREADS_BASE_URL)
    return None


# --- Bookshelf ---


@app.command()
def bookshelf(id: str, shelf: Optional[str] = None) -> None:
    print("getting books")


if __name__ == "__main__":
    app()
