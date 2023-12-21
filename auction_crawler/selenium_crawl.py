from selenium import webdriver
from selenium.webdriver.common.by import By
import time


driver = webdriver.Chrome()
driver.set_window_size(1500, 1400)

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
    elif time_to_break >= 20:
        print(f'Done crawling for {time_to_break} seconds')
        break
    last_height = new_height

# Cant make it to work
# driver.implicitly_wait(50)
#takes a screenshot after unchecking
# driver.save_screenshot()
data_elements = driver.find_elements(By.XPATH, "//p[contains(@class, 'md:mb-auto')]")
sum = 0
for element in data_elements:
    sum += 1
    print(element.text)
print(sum)

# Try to change container value to Baigiasi vėliausiai, for most recent items in page.
# xpath to Baigiasi vėliausiai - "//div[@class="Select__single-value css-qc6sy-singleValue']"

# xpath to auction end date - "//div[contains(@class, 'pl-9')]"
# xpath to starting price - //div[contains(@class, 'text-black') and contains(@class, 'font-poppins') and contains(@class, 'text-lg') and not(contains(@class, 'font-semibold'))]
# xpath to highest bid(may be null/0 or nothin) - //div[contains(@class, 'text-black') and contains(@class, 'font-poppins') and contains(@class, 'text-lg') and contains(@class, 'font-semibold')
# xpath to link end - '//a[contains(@href, '/auctions/') and not(contains(@class, 'hidden'))]'