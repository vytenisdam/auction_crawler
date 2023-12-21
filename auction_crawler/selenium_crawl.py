from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

webdriver_path = 'C:/Users/Vytenis/PycharmProjects/crawler_project/crawler_project/chromedriver-win64/chromedriver-win64'

driver = webdriver.Chrome()

url = 'https://foros.lt/auctions/'
# url = 'https://quotes.toscrape.com/'

driver.get(url)
checkbox = driver.find_element(By.XPATH, '//input[contains(@type, "checkbox")]')
if checkbox.is_selected():
    checkbox.click()
    driver.implicitly_wait(10)
    for i in driver.find_elements(By.XPATH, "//p[contains(@class, 'md:mb-auto')]"):
        print(i.text)
    # data_elements = driver.find_elements(By.XPATH, "//p[contains(@class, 'md:mb-auto')]")
# data_elements = driver.find_elements(By.XPATH, "//span[@class = 'text']")
#     for i in data_elements:
#         print(i.text)

driver.quit()