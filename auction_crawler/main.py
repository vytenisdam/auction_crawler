from selenium_crawl import (scroll_website, get_auction_link,
                            get_auction_end_dates, get_property_names,
                            get_property_price,get_highest_bids, data_format, driver)
from typing import Literal, Any
from csv_write import file_write
import time


def crawl_site(
        scroll_time: int,
        return_format: Literal['csv', 'records', 'string']) -> list[dict[str, Any]] | str:
    """All forest crawler functionality in one function. Returns a dictionary of crawled data."""
    start_time = time.monotonic()
    scroll_website(driver, scroll_time)
    names = get_property_names()
    prices = get_property_price()
    end_dates = get_auction_end_dates()
    highest_bids = get_highest_bids()
    links = get_auction_link()
    data = data_format(names, prices, end_dates, highest_bids, links)
    print('Example data in dict format: ')
    for i in data[:5]:
        print(i)
    end_time = time.monotonic()
    print(f'Scrolling and crawling took: {round((end_time - start_time), 2)} seconds')
    if return_format == 'records':
        return data
    elif return_format == 'string':
        return str(data)
    elif return_format == 'csv':
        file_write(data)


crawl_site(10, 'records')