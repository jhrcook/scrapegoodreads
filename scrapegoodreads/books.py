"""Scrape bookshelf information."""

import re
import time
from datetime import date, datetime
from typing import Any, Optional

from bs4 import BeautifulSoup, Tag
from pydantic import BaseModel
from selenium import webdriver

from scrapegoodreads import GOODREADS_URLS
from scrapegoodreads.exceptions import (
    InfiniteScrollBottomNotFound,
    UnknownDateFormatException,
)


class BookData(BaseModel):
    """Book data."""

    book_url: str
    cover_url: str
    full_title: str
    show_title: str
    author: str
    author_url: str
    isbn: Optional[str]
    isbn13: Optional[str]
    asin: Optional[str]
    avg_rating: float
    num_ratings: int
    date_pub: Optional[date]
    date_pub_edition: Optional[date]
    rating: Optional[int]
    # shelves


def _search_table_row_td(tr: Tag, class_: str, find: str) -> Tag:
    return tr.find("td", class_=class_).find(find)


def _get_table_row_td_value(tr: Tag, class_: str) -> str:
    return tr.find(class_=class_).find("div", class_="value").text.strip()


def _parse_dates(date_str: str) -> Optional[date]:
    if date_str == "unknown":
        return None
    fmt_date: Optional[date] = None
    for fmt in ["%b %Y", "%b %d, %Y", "%Y"]:
        try:
            fmt_date = datetime.strptime(date_str, fmt).date()
            return fmt_date
        except ValueError:
            pass
    raise UnknownDateFormatException(date_str)


def _extract_star_rating(star_tag: Tag) -> Optional[int]:
    stars_on = list(star_tag.find_all(class_="staticStar p10"))
    if len(stars_on) == 0:
        return None
    return len(stars_on)


def parse_book_table_row(tr: Tag) -> BookData:
    """Parse a single row of a book shelf table.

    Args:
        tr (Tag): Table row object.

    Returns:
        BookData: Book data.
    """
    _data: dict[str, Any] = {}

    # Cover
    cover_url = _search_table_row_td(tr, "field cover", "img")["src"]
    _data["cover_url"] = cover_url

    # Title
    title = _search_table_row_td(tr, "field title", "a")
    _data["full_title"] = title["title"]
    _data["show_title"] = title.text.strip()
    _data["book_url"] = title["href"]

    # Author
    author = _search_table_row_td(tr, "field author", "a")
    _data["author"] = author.text
    _data["author_url"] = author["href"]

    # ISBN, ISBN13, ASIN, average rating
    for field in ["isbn", "isbn13", "asin", "avg_rating"]:
        d = _get_table_row_td_value(tr, class_=f"field {field}")
        _data[field] = None if d == "" else d

    # Number of ratings
    n_ratings = _get_table_row_td_value(tr, class_="field num_ratings")
    _data["num_ratings"] = n_ratings.replace(",", "")

    # Date published, date published (edition)
    for field in ["date_pub", "date_pub_edition"]:
        d = _get_table_row_td_value(tr, class_=f"field {field}")
        _data[field] = _parse_dates(d)

    rating_info = tr.find("td", "field rating")
    if rating_info is None:
        raise ValueError("Could not find rating information.")
    _data["rating"] = _extract_star_rating(rating_info)

    return BookData(**_data)


def _infinite_scroll_status(soup: BeautifulSoup) -> tuple[int, int]:
    status = soup.find(id="infiniteStatus").text.strip()
    nums = [int(x) for x in re.findall("[0-9]+", status)]
    assert len(nums) == 2
    return (nums[0], nums[1])


def _make_driver() -> webdriver.Chrome:
    opts = webdriver.ChromeOptions()
    opts.binary_location = (
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
    )
    driver_path = "/usr/local/bin/chromedriver"
    opts.add_argument("--headless")
    driver = webdriver.Chrome(options=opts, executable_path=driver_path)
    return driver


# TODO: make option for which webdriver to use.


def beautiful_book_list(
    user_id: str, max_scrolls: int = 50, sleep_time: float = 2.0
) -> BeautifulSoup:
    """Get and parse the HTML for a Goodreads book shelf.

    Args:
        user_id (str): Goodreads user ID.
        max_scrolls (int, optional): Maximum number of scrolls for the infinite scroll
        of the webpage. Defaults to 50.
        sleep_time (float, optional): Delay between each scroll. Defaults to 2.0.

    Raises:
        InfiniteScrollBottomNotFound: If the bottom of the list is not reached.

    Returns:
        BeautifulSoup: The webpage of a book shelf after scrolling all the way to the
        bottom.
    """
    url = GOODREADS_URLS["list"] + user_id
    driver = _make_driver()
    driver.get(url)
    for _ in range(max_scrolls):
        driver.execute_script("window.scrollTo(1,50000)")
        soup = BeautifulSoup(driver.page_source, "html.parser")
        current_i, total = _infinite_scroll_status(soup)
        if current_i == total:
            return soup
        time.sleep(sleep_time)
    raise InfiniteScrollBottomNotFound("Try increasing maximum scrolls.")


def parse_book_shelf(books_soup: BeautifulSoup) -> list[BookData]:
    """Parse a Goodreads book shelf (list of books).

    Args:
        books_soup (BeautifulSoup): Goodreads book shelf.

    Returns:
        list[BookData]: List of books.
    """
    books_table = books_soup.find("table", id="books")
    table_body = books_table.find("tbody", id="booksBody")
    books: list[BookData] = []
    for table_row in table_body.find_all("tr"):
        books.append(parse_book_table_row(table_row))
    return books
