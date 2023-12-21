import requests
from auction_crawler.auction_crawler import get_to_node, get_links, headers, json_data

def test_links():
    """Checks all links of the auctions if their url's work. (If they give response code that is equal to 200"""
    for i in get_links(get_to_node(requests.post('https://miskoaukcionas.lt/graphql',headers=headers, json=json_data).json())):
        assert requests.get(i).status_code == 200

