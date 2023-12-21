import csv


def file_read():
    """Reads a file where the crawled data were put, to display it."""
    with open('crawl_data.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
