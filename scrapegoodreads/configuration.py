"""Configuration."""

import os
from itertools import product
from pathlib import Path
from typing import Optional

import yaml
from pydantic import BaseModel

from scrapegoodreads.webscraping_helpers import BuiltinWebDriver


class Configuration(BaseModel):
    """Goodreads web scraping interface configuration."""

    user_id: str
    user_email: str
    driver: Optional[BuiltinWebDriver] = None


def read_config(config_path: Path) -> Configuration:
    with open(config_path, "r") as file:
        data = yaml.safe_load(file)
    return Configuration(**data)


DEFAULT_CONFIG_PATHS = ["grscrape.yaml", "grscrape.yml"]
SEARCH_LOCATIONS: set[Optional[str]] = {".", os.getenv("HOME")}


def find_configuration_file() -> Optional[Path]:
    for loc, name in product(SEARCH_LOCATIONS, DEFAULT_CONFIG_PATHS):
        if loc is None:
            continue
        path = Path(loc) / name
        if path.exists():
            return path
    return None
