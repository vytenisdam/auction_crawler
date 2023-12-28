from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time


start_time = time.monotonic()

# Code for Chrome webdriver to work with headless mode
chrome_options = Options()
chrome_options.add_argument("--headless")
driver = webdriver.Chrome(options=chrome_options)
# driver.set_window_size(1200, 1200)


def scroll_website(time_limit: int) -> None:
    """Scrolls through website of forest auctions."""
    url = 'https://foros.lt/auctions/'

    driver.get(url)
    checkbox = driver.find_element(By.XPATH, '//input[contains(@type, "checkbox")]')

    if checkbox.is_selected():
        checkbox.click()
    # Maybe could be a better way to do this
    time.sleep(2)

    scroll_pause_time = 2

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")
    time_to_break = -2
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(scroll_pause_time)
        time_to_break += 2
        # Calculate new scroll height and compare with last scroll height
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
        prices.append(price)
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
            bids.append('0')
        else:
            bids.append(bid.text)
    return bids


def get_auction_link() -> list:
    """Returns link for each crawled auction."""
    auction_link_ends = driver.find_elements(By.XPATH, "//a[contains(@href, '/auctions/') and not(contains(@class, 'hidden'))]")
    links = []
    for link in auction_link_ends:
        links.append(link.get_attribute("href"))
    return links

# scroll time != crawl time, is it okay to leave scroll time limit or time limit should be for all processes in crawling.


scroll_website(10)
a = get_auction_link()
print(a)
end_time = time.monotonic()
print(end_time-start_time)
# Try to change container value to Baigiasi vėliausiai, for most recent items in page.
# xpath to Baigiasi vėliausiai - "//div[@class="Select__single-value css-qc6sy-singleValue']"
