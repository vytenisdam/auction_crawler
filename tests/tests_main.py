import pytest
import requests
from auction_crawler.selenium_crawl import get_auction_link


def test_links():
    """Checks all links of the auctions if their url's work. (If they give response code that is equal to 200"""
    for i in get_auction_link():
        assert requests.get(i).status_code == 200

