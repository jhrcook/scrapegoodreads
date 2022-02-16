"""General utilities and helpers."""

from enum import Enum
from typing import Union

from selenium import webdriver

ParamsDict = dict[str, Union[None, str, float, bool]]


class WebRequestMethod(Enum):
    """Webpage request method."""

    REQUESTS = "REQUESTS"
    SELENIUM = "SELENIUM"


def headless_chrome_driver() -> webdriver.Chrome:
    opts = webdriver.ChromeOptions()
    opts.binary_location = (
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    )
    driver_path = "/usr/local/bin/chromedriver"
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts, executable_path=driver_path)
    return driver
