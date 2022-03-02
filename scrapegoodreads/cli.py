"""Scrapegoodreads main entrypoint."""

import logging
import time
from pathlib import Path
from typing import Optional

import bleach
import keyring
import typer
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver as RemoteWebDriver

from scrapegoodreads import GOODREADS_URLS, logger
from scrapegoodreads.configuration import (
    Configuration,
    find_configuration_file,
    read_config,
)
from scrapegoodreads.exceptions import InputException
from scrapegoodreads.webscraping_helpers import BuiltinWebDriver, make_builtin_driver

# --- CLI setup ---


app = typer.Typer()
logger.setLevel(logging.INFO)


# --- Utilities ---


def _default_web_driver() -> BuiltinWebDriver:
    return BuiltinWebDriver.BRAVE


# --- Log-in ---


def _login_password() -> Optional[str]:
    key_service_name, key_user = "goodreads-webscraping", "user"
    pswd = keyring.get_password(key_service_name, key_user)
    if pswd is not None:
        return pswd

    pswd = bleach.clean(input("password (leave blank if none): ")).strip()
    if pswd is None or pswd == "":
        return None

    keyring.set_password(key_service_name, key_user, pswd)
    return pswd


def _select_remember_me_button(driver: RemoteWebDriver) -> None:
    remember_me_button = driver.find_element(By.ID, "remember_me")
    if not remember_me_button.is_selected():
        remember_me_button.click()
    return None


def _input_email(driver: RemoteWebDriver, email: str) -> None:
    email_element = driver.find_element(By.ID, "user_email")
    email_element.clear()
    email_element.send_keys(email)
    return None


def _input_password(driver: RemoteWebDriver, password: str) -> None:
    password_element = driver.find_element(By.ID, "user_password")
    password_element.clear()
    password_element.send_keys(password)
    return None


class NotLoggedInException(BaseException):
    """Unsuccessful log-in."""

    ...


def goodreads_login(driver: RemoteWebDriver, email: str) -> None:
    driver.get(GOODREADS_URLS["sign-in"])
    _select_remember_me_button(driver)
    _input_email(driver, email)
    if (pswd := _login_password()) is not None:
        _input_password(driver, pswd)
        driver.find_element(By.NAME, "next").click()
    else:
        input("Sign in to Goodreads in the browser and hit 'Enter' when done: ")
    return None


# --- Profile ---


def _check_successful_login(driver: RemoteWebDriver) -> None:
    if driver.current_url == GOODREADS_URLS["sign-in"]:
        driver.quit()
        logger.error("Currently at sign-in page.")
        raise NotLoggedInException()
    try:
        driver.find_element(By.ID, "signIn")
        driver.quit()
        logger.error("Found sign-in box.")
        raise NotLoggedInException()
    except NoSuchElementException:
        ...

    logger.info("Successful log-in.")
    return None


@app.command()
def profile(
    config: Optional[Path] = None,
    id: Optional[str] = None,
    email: Optional[str] = None,
    driver: Optional[BuiltinWebDriver] = None,
) -> None:
    config = config if config is not None else find_configuration_file()
    gr_config: Configuration
    if config is not None:
        gr_config = read_config(config)
    elif id is not None and email is not None:
        gr_config = Configuration(user_id=id, user_email=email, driver=driver)
    else:
        msg = "Must supply either a configuration file or user ID & email."
        raise InputException(msg)

    if gr_config.driver is None:
        gr_config.driver = _default_web_driver()
        logger.info(f"Using default web driver '{gr_config.driver.value}'")

    web_driver = make_builtin_driver(gr_config.driver)
    goodreads_login(web_driver, email=gr_config.user_email)
    _check_successful_login(web_driver)

    # TODO: web-scraping...

    time.sleep(2)
    web_driver.quit()
    logger.info("Goodreads web-scraping complete.")
    return None


# --- Bookshelf ---


@app.command()
def bookshelf(id: str, shelf: Optional[str] = None) -> None:
    raise NotImplementedError("Parsing bookshelves has yet to be implemented.")


if __name__ == "__main__":
    app()
