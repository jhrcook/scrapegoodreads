import pytest

from scrapegoodreads import books
from scrapegoodreads.exceptions import InfiniteScrollBottomNotFound


def test_get_list_of_books(jhc_user_id: str) -> None:
    book_soup = books.beautiful_book_list(user_id=jhc_user_id)
    book_list = books.parse_book_shelf(book_soup)
    assert len(book_list) > 0


def test_error_if_not_scrolled_far_enough(jhc_user_id: str) -> None:
    with pytest.raises(InfiniteScrollBottomNotFound):
        _ = books.beautiful_book_list(user_id=jhc_user_id, max_scrolls=2)
