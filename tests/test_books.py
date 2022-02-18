import pytest

from scrapegoodreads import books
from scrapegoodreads.exceptions import InfiniteScrollBottomNotFound
from scrapegoodreads.webscraping_helpers import BuiltinWebDriver, WebRequestMethod


@pytest.mark.parametrize("method", WebRequestMethod)
def test_get_list_of_books(jhc_user_id: str, method: WebRequestMethod) -> None:
    book_soup, web_driver = books.beautiful_book_list(
        user_id=jhc_user_id, method=method, driver=BuiltinWebDriver.HEADLESS_CHROME
    )
    if web_driver is not None:
        web_driver.close()
    book_list = books.parse_book_shelf(book_soup)
    assert len(book_list) > 5


@pytest.mark.parametrize("driver", BuiltinWebDriver)
def test_get_list_of_books_with_drivers(
    jhc_user_id: str, driver: BuiltinWebDriver
) -> None:
    book_soup, webdriver = books.beautiful_book_list(
        user_id=jhc_user_id,
        method=WebRequestMethod.SELENIUM,
        driver=driver,
        shelf="greats",  # shorter list
    )
    if webdriver is not None:
        webdriver.close()
    book_list = books.parse_book_shelf(book_soup)
    assert len(book_list) > 5


def test_errors_if_no_driver(jhc_user_id: str) -> None:
    with pytest.raises(BaseException):
        _ = books.beautiful_book_list(
            user_id=jhc_user_id, method=WebRequestMethod.SELENIUM
        )


def test_error_if_not_scrolled_far_enough(jhc_user_id: str) -> None:
    with pytest.raises(InfiniteScrollBottomNotFound):
        _ = books.beautiful_book_list(
            user_id=jhc_user_id,
            method=WebRequestMethod.SELENIUM,
            driver=BuiltinWebDriver.HEADLESS_CHROME,
            max_scrolls=2,
        )


def test_get_books_from_specific_shelf(jhc_user_id: str) -> None:
    book_soup, _ = books.beautiful_book_list(
        user_id=jhc_user_id, method=WebRequestMethod.REQUESTS, shelf="greats"
    )
    book_list = books.parse_book_shelf(book_soup)
    assert len(book_list) > 5
