"""Scrape profile information."""

import re

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel

from scrapegoodreads import GOODREADS_URLS


class UserStatistics(BaseModel):
    """User statistics."""

    num_ratings: int
    avg_rating: float
    num_reviews: int


def extract_user_stats(profile_soup: BeautifulSoup) -> UserStatistics:
    user_stats = profile_soup.find(class_="profilePageUserStatsInfo").text.splitlines()
    user_stats = [x.strip() for x in user_stats if x.strip() != ""]
    assert len(user_stats) == 3, "Unknown data in user info."
    num_ratings = re.findall("[0-9]+", user_stats[0])[0]
    avg_rating = re.findall("[0-9|\\.]+", user_stats[1])[0]
    num_reviews = re.findall("[0-9]+", user_stats[2])[0]
    return UserStatistics(
        num_ratings=num_ratings, avg_rating=avg_rating, num_reviews=num_reviews
    )


def get_profile(user_id: int, username: str) -> requests.Response:
    url = GOODREADS_URLS["user"] + str(user_id)
    res = requests.get(url=url)
    return res


def beautiful_profile(user_id: int, username: str) -> BeautifulSoup:
    res = get_profile(user_id=user_id, username=username)
    soup = BeautifulSoup(res.content, "html.parser")
    return soup
