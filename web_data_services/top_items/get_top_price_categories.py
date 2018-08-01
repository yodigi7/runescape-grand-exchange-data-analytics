from bs4 import BeautifulSoup
import py_logging
import requests

from get_config import get_config


def get_top_price_fall_names() -> list:
    config = get_config()
    return get_top_price(config['DEFAULT']['TopPriceFallsUrl'])


def get_top_price_rise_names() -> list:
    config = get_config()
    return get_top_price(config['DEFAULT']['TopPriceRisesUrl'])


def get_top_price_value_names() -> list:
    config = get_config()
    return get_top_price(config['DEFAULT']['TopPriceValuesUrl'])


def get_top_price_most_traded_names() -> list:
    config = get_config()
    return get_top_price(config['DEFAULT']['TopPriceMostTradedUrl'])


def get_top_price(url: str) -> list:
    html_text = requests.get(url).text
    soup = BeautifulSoup(html_text, 'lxml')
    rows = soup.find('table').find('tbody').find_all('tr')
    list_of_ids = [row.find('td').find('a').find('img', title=True)['title'] for row in rows]
    return list_of_ids


if __name__ == '__main__':
    print(get_top_price_fall_names())
    print(get_top_price_rise_names())
    print(get_top_price_value_names())
