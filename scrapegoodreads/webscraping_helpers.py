"""General utilities and helpers."""

import os
from enum import Enum
from pathlib import Path
from typing import Callable, Final, Iterable, Optional, Union

from selenium import webdriver
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

ParamsDict = dict[str, Union[None, str, float, bool]]


class WebRequestMethod(Enum):
    """Webpage request method."""

    REQUESTS = "REQUESTS"
    SELENIUM = "SELENIUM"


def chrome_driver(headless: bool = False) -> webdriver.Chrome:
    """Create a Chrome web driver.

    Args:
        headless (bool, optional): Create headless driver? Defaults to False.

    Returns:
        webdriver.Chrome: Chrome web driver.
    """
    opts = webdriver.ChromeOptions()
    if headless:
        opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts)
    return driver


def headless_chrome_driver() -> webdriver.Chrome:
    """Create a headless Chrome web driver.

    Returns:
        webdriver.Chrome: Headless chromium web driver.
    """
    return chrome_driver(headless=True)


def _search_env_and_some_default_locations(
    env_var: str, search_paths: Iterable[str]
) -> Optional[str]:
    if (path := os.getenv(env_var)) is not None:
        return path

    for search_path in search_paths:
        if Path(search_path).exists():
            return search_path

    return None


def _check_path(path: Optional[str], env_var: str, name: str) -> str:
    if path is None:
        raise ValueError(f"Cannot locate {name} - set env var '{env_var}'.")
    elif not Path(path).exists():
        raise FileNotFoundError(f"Path to {name} does not exist: '{path}'.")
    return path


def _brave_app_location() -> str:
    env_var = "BRAVE_PATH"
    search_paths = {"/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"}
    brave_path = _search_env_and_some_default_locations(env_var, search_paths)
    return _check_path(brave_path, env_var=env_var, name="Brave app")


def _chrome_driver_path() -> str:
    env_var = "CHROMIUM_PATH"
    search_paths = {"/usr/local/bin/chromedriver"}
    chrome_path = _search_env_and_some_default_locations(env_var, search_paths)
    return _check_path(chrome_path, env_var=env_var, name="chrome driver")


def brave_driver(headless: bool = False) -> webdriver.Chrome:
    """Create a Brave web driver.

    Args:
        headless (bool, optional): Create headless driver? Defaults to False.

    Returns:
        webdriver.Chrome: Brave web driver.
    """
    opts = webdriver.ChromeOptions()
    opts.binary_location = _brave_app_location()
    driver_path = _chrome_driver_path()
    if headless:
        opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts, executable_path=driver_path)
    return driver


def headless_brave_driver() -> webdriver.Chrome:
    """Create a headless Brave (chromium) web driver.

    Returns:
        webdriver.Chrome: Headless chromium web driver.
    """
    return brave_driver(headless=True)


def safari_driver() -> webdriver.Safari:
    """Create a Safari web driver object.

    Returns:
        webdriver.Safari: Basic Safari web driver.
    """
    return webdriver.Safari()


class BuiltinWebDriver(Enum):
    """Supported built-in web drivers."""

    HEADLESS_CHROME = "HEADLESS_CHROME"
    HEADLESS_BRAVE = "HEADLESS_BRAVE"
    CHROME = "CHROME"
    BRAVE = "BRAVE"
    SAFARI = "SAFARI"


def make_builtin_driver(opt: BuiltinWebDriver) -> RemoteWebDriver:
    """Create a pre-specified web driver.

    Args:
        opt (BuiltinWebDriver): Web driver option.

    Returns:
        RemoteWebDriver: Selenium web driver.
    """
    _driver_lookup: Final[dict[BuiltinWebDriver, Callable[[], RemoteWebDriver]]] = {
        BuiltinWebDriver.HEADLESS_CHROME: headless_chrome_driver,
        BuiltinWebDriver.HEADLESS_BRAVE: headless_brave_driver,
        BuiltinWebDriver.CHROME: chrome_driver,
        BuiltinWebDriver.BRAVE: brave_driver,
        BuiltinWebDriver.SAFARI: safari_driver,
    }
    return _driver_lookup[opt]()
