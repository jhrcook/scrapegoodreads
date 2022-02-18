# A web scraping tool for Goodreads

**Just focus on features that I want.**

## To-Do

- doc: note use of selenium in documentation
- doc: layout general idea of the package and that it is relatively simple and features are added as I want them
  - main point is to get the data into your hands
- feat: get reading activity from Goodreads

## Features

### Collect books from a bookshelf

It is easy to get all of the books from a user's bookshelf.

```python
from pprint import pprint
from scrapegoodreads import books

soup_shelf = books.beautiful_book_list(user_id="144433284")
book_shelf = books.parse_book_shelf(soup_shelf)
len(book_shelf)
#> 228
type(book_shelf[0])
# <class 'scrapegoodreads.books.BookData'>>
```

The object returned is a list of `BookData`, so any common Python list operation can be applied.
For example, I can search for my favorite book *Rascal* by Sterling North.

```python
# Get my favorite book "Rascal" by Stirling North.
rascal = list(filter(lambda b: b.full_title == "Rascal", book_shelf))[0]
pprint(rascal.dict())
# {
#   'asin': None,
#   'author': 'North, Sterling',
#   'author_url': '/author/show/43889.Sterling_North',
#   'avg_rating': 4.15,
#   'book_url': '/book/show/967511.Rascal',
#   'cover_url': 'https://i.gr-assets.com/images/S/compressed.photo.goodreads.com/books/1309211625l/967511._SY75_.jpg',
#   'date_pub': datetime.date(1963, 1, 1),
#   'date_pub_edition': datetime.date(1998, 4, 28),
#   'full_title': 'Rascal',
#   'isbn': '0140344454',
#   'isbn13': '9780140344455',
#   'num_ratings': 12763,
#   'rating': 5,
#   'show_title': 'Rascal'
# }
```

Or I can get all of the Hemingway novels I've read and show my ratings.

```python
from typing import Optional


def _make_stars(n_stars: Optional[int]) -> str:
    if n_stars is None:
        return "not read"
    return "⭐️" * n_stars + " " * (5 - n_stars)


hemingway = filter(
    lambda b: "hemingway" in b.author.lower() and b.rating is not None, book_shelf
)
for eh in hemingway:
    print(f"{_make_stars(eh.rating)} {eh.show_title}")
```

We can also scrape a specific book shelf for a user.
Below I show all of the books on my "greats" book shelf.

```python
greats_soup_shelf = books.beautiful_book_list(user_id=JHC_ID, shelf="greats")
greats_book_shelf = books.parse_book_shelf(greats_soup_shelf)
greats_book_shelf.sort(key=lambda b: b.date_pub or date.today())
for book in greats_book_shelf:
    print(f"'{book.show_title}' by {book.author}")
# 'Twelve Years a Slave' by Northup, Solomon
# 'The Elements of Style' by Strunk Jr., William
# 'Man's Search for Meaning' by Frankl, Viktor E.
# 'The Old Man and the Sea' by Hemingway, Ernest
# 'Capitalism and Freedom' by Friedman, Milton
# 'Rascal' by North, Sterling
# 'The Design of Everyday Things' by Norman, Donald A.
# 'The Mental Game of Baseball: A Guide to Peak Performance' by Dorfman, H.A.
# 'Happiness Is a Serious Problem: A Human Nature Repair Manual' by Prager, Dennis
```

Note that Goodreads uses an "infinite scroll" webpage when you are not logged in, so the 'selenium' package is required to automate the scrolling process until all books are loaded.
If you do not want this feature and instead just use 'requests,' only a subset of the books are available (the default is 30 at the time of writing).
To only use requests, pass it as the argument for `method` as shown below.

```python
from scrapegoodreads import books
from scrapegoodreads.webscraping_helpers import WebRequestMethod

soup_shelf_limited = books.beautiful_book_list(
    user_id="144433284", method=WebRequestMethod.REQUESTS
)
book_shelf_limited = books.parse_book_shelf(soup_shelf_limited)
len(book_shelf_limited)
```

Alternatively, if you want to use 'selenium' but not the default web driver (currently a headless chrome browser), you can supply your own.

```python
from selenium import webdriver

opts = webdriver.ChromeOptions()
opts.binary_location = (
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"
)
driver_path = "/usr/local/bin/chromedriver"
opts.add_argument("--headless")
brave_driver = webdriver.Chrome(options=opts, executable_path=driver_path)

soup_shelf_limited = books.beautiful_book_list(user_id="144433284", driver=brave_driver)
```
