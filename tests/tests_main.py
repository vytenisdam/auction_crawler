import unittest
from unittest.mock import Mock, patch
from auction_crawler.selenium_crawl import scroll_website, get_auction_link, driver, format_to_float
import requests
#

class TestScrollWebsite(unittest.TestCase):
    @patch('auction_crawler.selenium_crawl.webdriver.Chrome')
    def test_scroll_website_checkbox_click(self, mock_driver_class):
        # Mock the driver instance and its methods
        mock_driver = mock_driver_class.return_value
        mock_checkbox = Mock()
        # Mock the find_element method to return the checkbox mock
        mock_driver.find_element.return_value = mock_checkbox
        # Call the function with the mock driver
        scroll_website(mock_driver, 10)
        # Assert that the checkbox click method was called
        mock_checkbox.click.assert_called_once()


class TestFormatToFloat(unittest.TestCase):
    def test_format_to_float(self):
        input_string = '4 575,54 €'
        expected_result = 4575.54

        result = format_to_float(input_string)
        self.assertEqual(result, expected_result)


def test_links():
    """Checks all links of the auctions if their url's work. (If they give response code that is equal to 200"""
    scroll_website(driver, 2)
    for i in get_auction_link():
        assert requests.get(i).status_code == 200


if __name__ == '__main__':
    unittest.main()
