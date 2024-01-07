import unittest
from unittest.mock import Mock, patch
from auction_crawler.selenium_crawl import scroll_website, get_auction_link, driver, format_to_float, data_format
import requests


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
        input_string = [None, '4 575,54 €', '1234 56 $', 1235]
        expected_result = [0.0, 4575.54, 123456, 1235]

        result = [format_to_float(i) for i in input_string]
        self.assertEqual(result, expected_result)


class TestDataFormat(unittest.TestCase):
    def test_data_format(self):
        names = ['Property 1', 'Property 2', 125, None]
        prices = [1000, 2000, 'number', None]
        end_dates = ['2022-01-01', '2022-02-01', None, 125]
        bids = [800, 1800, 'number', None]
        links = ['http://property1.com', 'http://property2.com', 1235, None]

        expected_result = [
            {'Property name': 'Property 1',
             'Property price': 1000,
             'Auction end date': '2022-01-01',
             'Highest bid': 800,
             'Auction link': 'http://property1.com'},
            {'Property name': 'Property 2',
             'Property price': 2000,
             'Auction end date': '2022-02-01',
             'Highest bid': 1800,
             'Auction link': 'http://property2.com'},
            {'Property name': 125,
             'Property price': 'number',
             'Auction end date': None,
             'Highest bid': 'number', 'Auction link': 1235},
            {'Property name': None,
             'Property price': None,
             'Auction end date': 125,
             'Highest bid': None,
             'Auction link': None}
        ]

        result = data_format(names, prices, end_dates, bids, links)
        self.assertEqual(result, expected_result)


def test_links():
    """Checks all links of the auctions if their urls work. (If they give response code that is equal to 200"""
    scroll_website(driver, 2)
    for i in get_auction_link():
        if i is not None:
            assert requests.get(i).status_code == 200


if __name__ == '__main__':
    unittest.main()
