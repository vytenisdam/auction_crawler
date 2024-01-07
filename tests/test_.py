import unittest
from selenium.webdriver.common.by import By
from unittest.mock import MagicMock, Mock, patch
from auction_crawler.selenium_crawl import (scroll_website, get_auction_link, driver,
                                            format_to_float, data_format, get_property_names)
from auction_crawler.csv_write import file_write
import os
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


class TestGetPropertyNames(unittest.TestCase):

    @patch('auction_crawler.selenium_crawl.driver.find_elements')
    def test_get_property_names(self, mock_find_elements):
        # Mock the behavior of find_elements
        mock_element1 = MagicMock()
        mock_element1.text = 'Property 1'
        mock_element2 = MagicMock()
        mock_element2.text = 'Property 2'
        mock_find_elements.return_value = [mock_element1, mock_element2]
        # Call the function
        result = get_property_names()
        # Assert the expected result
        expected_result = ['Property 1', 'Property 2']
        self.assertEqual(result, expected_result)
        # Assert that find_elements was called with the correct arguments
        mock_find_elements.assert_called_once_with(By.XPATH, "//p[contains(@class, 'md:mb-auto')]")


def test_links():
    """Checks all links of the auctions if their urls work. (If they give response code that is equal to 200"""
    scroll_website(driver, 2)
    for i in get_auction_link():
        if i is not None:
            assert requests.get(i).status_code == 200


class TestFileWrite(unittest.TestCase):
    def setUp(self):
        # This method is called before each test method.
        pass

    def tearDown(self):
        # This method is called after each test method.
        # Clean up or revert changes made during the test if needed.
        if os.path.exists('crawl_data.csv'):
            os.remove('crawl_data.csv')

    def test_file_creation(self):
        # Call the file_write function.
        data_to_write = [{'Property name': 'Test Property', 'Property price': 1000, 'Auction end date': '2024-01-01',
                          'Highest bid': 800, 'Auction link': 'http://example.com/auction/1'}]
        file_write(data_to_write)
        # Check if the file is created.
        self.assertTrue(os.path.exists('crawl_data.csv'))


if __name__ == '__main__':
    unittest.main()
