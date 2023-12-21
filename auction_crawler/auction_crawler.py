import requests

headers = {
    'authority': 'miskoaukcionas.lt',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9',
    'apollographql-client-name': 'foros',
    'content-type': 'application/json',
    # 'cookie': '_gcl_au=1.1.853228723.1702577507; _hjFirstSeen=1; _hjIncludedInSessionSample_2433611=1; _hjSession_2433611=eyJpZCI6Ijk2NDA4MjZiLTJmYzItNDMyOC04YWYwLTc1YjcyYWFlZTk2MiIsImMiOjE3MDI1Nzc1MDcwMDcsInMiOjEsInIiOjAsInNiIjowfQ==; _hjSessionUser_2433611=eyJpZCI6IjA1OWEwZTVhLWU4OWEtNTY1ZS1hNjYzLTk2ZjdiZDdkNzU5OSIsImNyZWF0ZWQiOjE3MDI1Nzc1MDcwMDUsImV4aXN0aW5nIjp0cnVlfQ==; _hjAbsoluteSessionInProgress=0; _gid=GA1.2.1178041178.1702577507; _fbp=fb.1.1702577507451.591394816; CookieConsent=true; _ga=GA1.1.912892948.1702577507; _ga_0YNZF0LFEH=GS1.1.1702582691.2.1.1702583778.60.0.0',
    'domain': 'miskoaukcionas.lt',
    'origin': 'https://miskoaukcionas.lt',
    'referer': 'https://miskoaukcionas.lt/auctions',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
}

json_data = [
    {
        'operationName': 'ListAuctions',
        'variables': {
            'first': 100,
            # 'auctionOpen': True,
            'order': {
                'endTime': 'desc',
                # 'currentBidPrice': 'desc',
            },
        },
        'extensions': {
            'persistedQuery': {
                'version': 1,
                'sha256Hash': '211d6c8492a72083617d24d253d3f430dc6a25b3aa96f88cd40f7acaa2f7ff08',
            },
        },
    },
]


def forest_auction_crawler():
    """Crawls through a website: https:/miskoaukcionas.lt and returns active auctions,
     their names, prices, auction end dates and auction links."""
    response = get_response('https://miskoaukcionas.lt/graphql')

    data = get_to_node(response.json())

    property_names = get_title(data)
    property_prices = get_prices(data)
    auction_end = get_auction_end(data)
    links_to_auction = get_links(data)
    data_to_write = data_format(property_names, property_prices, auction_end, links_to_auction)
    file_write(data_to_write)

def get_response(url):
    return requests.post(url, headers=headers, json=json_data)


def get_to_node(data):
    new_data = []
    for i in data:
        for j in i['data']['auctions']['edges']:
            new_data.append(j['node'])
    return new_data


def get_title(path_to_node):
    property_names = []
    for i in path_to_node:
        property_names.append(i['title'])
    return property_names


def get_prices(path_to_node):
    auction_end = []
    for i in path_to_node:
        auction_end.append(str(i['endTime'])[:10:])
    return auction_end


def get_links(path_to_node):
    links_to_auction = []
    for i in path_to_node:
        links_to_auction.append('https://miskoaukcionas.lt/auctions/' + i['id'])
    return links_to_auction


def get_auction_end(path_to_node):
    property_names = []
    for i in path_to_node:
        property_names.append(i['title'])
    return property_names


def data_format(property_names,property_prices, auction_end, link_to_auction):
    """Formats crawled data dictionary."""
    return [
        {
            'Property name': name,
            'Property price': price,
            'Auction end date': date,
            'Auction link': link
        }
        for name, price, date, link in zip(property_names, property_prices, auction_end, link_to_auction)
    ]

