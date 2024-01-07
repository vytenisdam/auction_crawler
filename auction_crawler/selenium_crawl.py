from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import requests

import time


# start_time = time.monotonic()

# Code for Chrome webdriver to work with headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
driver.set_window_size(1200, 1200)


def scroll_website(driver, time_limit: int) -> None:
    """Scrolls through the website of forest auctions."""
    url = 'https://foros.lt/auctions/'

    driver.get(url)
    checkbox = driver.find_element(By.XPATH, '//input[contains(@type, "checkbox")]')

    if checkbox.is_selected():
        checkbox.click()
    time.sleep(2)

    scroll_pause_time = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    time_to_break = -2
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load the page
        time.sleep(scroll_pause_time)
        time_to_break += 2
        # Calculate new scroll height and compare with the last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            print('done crawling end of the page')
            break
        elif time_to_break >= time_limit:
            print(f'Done crawling for {time_to_break} seconds')
            break
        last_height = new_height


def get_property_names() -> list:
    """Returns list of all crawled forest property names."""
    property_names = driver.find_elements(By.XPATH, "//p[contains(@class, 'md:mb-auto')]")
    names = []
    for name in property_names:
        names.append(name.text)
    return names


def get_property_price() -> list:
    """Returns list of all crawled forest property prices."""
    property_prices = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-black') and contains(@class, 'font-poppins') and contains(@class, 'text-lg') and not(contains(@class, 'font-semibold'))]")
    prices = []
    for price in property_prices:
        prices.append(format_to_float(price.text))
    return prices


def get_auction_end_dates() -> list:
    """Returns list of all crawled auction end dates."""
    auction_end_dates = driver.find_elements(By.XPATH, "//div[contains(@class, 'pl-9')]")
    end_dates = []
    for date in auction_end_dates:
        end_dates.append(date.text[:10:])
    return end_dates


def get_highest_bids() -> list:
    """Returns list of all crawled forest auction bids or 0 if auction didn't had a bid."""
    highest_bids = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-black') and contains(@class, 'font-poppins') and contains(@class, 'text-lg') and contains(@class, 'font-semibold')]")
    bids = []
    for bid in highest_bids:
        if bid.text == '':
            bids.append(0.0)
        else:
            bids.append(format_to_float(bid.text))
    return bids


def get_auction_link() -> list:
    """Returns link for each crawled auction."""
    auction_link_ends = driver.find_elements(By.XPATH, "//a[contains(@href, '/auctions/') and not(contains(@class, 'hidden'))]")
    links = []
    for link in auction_link_ends:
        links.append(link.get_attribute("href"))
    return links


def data_format(names: list, prices: list, end_dates: list, bids: list, links: list) -> list:
    """Joins the crawled data of each auction to dictionary and returns a list of dictionaries."""
    return [
        {
            'Property name': name,
            'Property price': price,
            'Auction end date': date,
            'Highest bid': bid,
            'Auction link': link
        }
        for name, price, date, bid, link in zip(names, prices, end_dates, bids, links)]


def format_to_float(to_be_number: str) -> float:
    """Formats string format '00 000,00 €', to float type."""
    if to_be_number is None:
        return 0.0
    elif type(to_be_number) is int:
        return float(to_be_number)
    else:
        numeric_string = to_be_number.replace(' ', '').replace(',', '.')
        return float(numeric_string[:-1])


def crawl_site() -> None:
    """All forest crawler functionality in one function. Returns a dictionary of crawled data."""

    start_time = time.monotonic()
    scroll_website(10)
    names = get_property_names()
    prices = get_property_price()
    end_dates = get_auction_end_dates()
    highest_bids = get_highest_bids()
    links = get_auction_link()

    # print(type(data_format(names, prices, end_dates, highest_bids, links)[0]))
    data = data_format(names, prices, end_dates, highest_bids, links)
    end_time = time.monotonic()
    print(data)
    print(end_time - start_time)


# # Try to change container value to Baigiasi vėliausiai, for most recent items in page.
# # xpath to Baigiasi vėliausiai - "//div[@class="Select__single-value css-qc6sy-singleValue']"

