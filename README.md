# A web-scraping tool for Goodreads

**A Python library for scraping data from [Goodreads](https://www.goodreads.com).**

[![goodreads](https://img.shields.io/badge/scrape-Goodreads-372213.svg?style=flat&logo=goodreads&logoColor=#262626)](https://www.goodreads.com)
[![python](https://img.shields.io/badge/Python-3.9-3776AB.svg?style=flat&logo=python&logoColor=white)](https://www.python.org)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)

> This project is still a work-in-progress.

## To-Do

1. logging-in system (manually or email + password stored locally)
1. command to get info from personal account
1. command to scrape all books

## Install

```bash
pip install git+https://github.com/jhrcook/scrapegoodreads.git
```

This library uses ['selenium'](https://pypi.org/project/selenium/) so make sure that you have one of the supported web browsers installed to use those features.
I have tried to include documentation about how to use the web drivers, but please open an [Issue](https://github.com/jhrcook/scrapegoodreads/issues) if you have any questions or run into problems.

## Use

Goodreads has closed its API to the public, so until then, we have to use web-scraping to collect data from the website.
This package methodically works through the website and collects whatever data the user wants.

Unfortunately, a lot of the interesting information and user-specific information can only be accessed when logged in to the service.
Therefore, the signing in process has to be included in a lot of the workflows.

- add info about config file
