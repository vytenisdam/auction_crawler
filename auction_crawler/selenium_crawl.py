from selenium import webdriver
from selenium.webdriver.common.by import By

import time


driver = webdriver.Chrome()
driver.set_window_size(1500, 1400)

url = 'https://foros.lt/auctions/'

driver.get(url)
checkbox = driver.find_element(By.XPATH, '//input[contains(@type, "checkbox")]')
#takes a screenshot before unchecking
# driver.save_screenshot('1.png')
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
# driver.save_screenshot('2.png')
data_elements = driver.find_elements(By.XPATH, "//p[contains(@class, 'md:mb-auto')]")
sum = 0
for element in data_elements:
    sum += 1
    print(element.text)
print(sum)


