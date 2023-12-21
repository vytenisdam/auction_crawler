from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.set_window_size(1200, 1200)

url = 'https://foros.lt/auctions/'

driver.get(url)
checkbox = driver.find_element(By.XPATH, '//input[contains(@type, "checkbox")]')
#takes a screenshot before unchecking checkbox
# driver.save_screenshot()
if checkbox.is_selected():
    checkbox.click()
# Should be a better option
time.sleep(2)

SCROLL_PAUSE_TIME = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")
time_to_break = -2
while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)
    time_to_break += 2
    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        print('done crawling end of the page')
        break
    elif time_to_break >= 2:
        print(f'Done crawling for {time_to_break} seconds')
        break
    last_height = new_height

# Cant make it to work
# driver.implicitly_wait(50)
#takes a screenshot after unchecking
# driver.save_screenshot()


def get_property_names() -> list:
    property_names = driver.find_elements(By.XPATH, "//p[contains(@class, 'md:mb-auto')]")
    names = []
    for name in property_names:
        names.append(name.text)
    return names


def get_property_price() -> list:
    property_prices = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-black') and contains(@class, 'font-poppins') and contains(@class, 'text-lg') and not(contains(@class, 'font-semibold'))]")
    prices = []
    for price in property_prices:
        prices.append(price)
    return prices


def get_auction_end_dates() -> list:
    auction_end_dates = driver.find_elements(By.XPATH, "//div[contains(@class, 'pl-9')]")
    end_dates = []
    for date in auction_end_dates:
        end_dates.append(date.text[:10:])
    return end_dates


def get_highest_bids() -> list:
    highest_bids = driver.find_elements(By.XPATH, "//div[contains(@class, 'text-black') and contains(@class, 'font-poppins') and contains(@class, 'text-lg') and contains(@class, 'font-semibold')]")
    bids = []
    for bid in highest_bids:
        if bid.text == '':
            bids.append('0')
        else:
            bids.append(bid.text)
    return bids


def get_auction_link() -> list:
    auction_link_ends = driver.find_elements(By.XPATH, "//a[contains(@href, '/auctions/') and not(contains(@class, 'hidden'))]")
    links = []
    for link in auction_link_ends:
        links.append(link.get_attribute("href"))
    return links



# Try to change container value to Baigiasi vėliausiai, for most recent items in page.
# xpath to Baigiasi vėliausiai - "//div[@class="Select__single-value css-qc6sy-singleValue']"
