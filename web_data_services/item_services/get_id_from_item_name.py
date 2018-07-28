from get_config import get_config
from bs4 import BeautifulSoup
import py_logging
import requests
import urllib
import os


def get_id_from_name(name: str, setting: str = 'DEFAULT') -> int:
    logger = py_logging.create_logger('get_id_from_item_name', '{}get_id_from_item_name.log'.format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    config = get_config()

    html_page = requests.get(
        config[setting]['NameToIdBaseUrl'] +
        urllib.parse.quote_plus(name)).text
    logger.info("Sent request off to find the id for: {}".format(name))

    soup = BeautifulSoup(html_page, 'html.parser')
    return soup.find('table', {"class": "table"}) \
               .find_all('tr')[1] \
               .find('td') \
               .getText()


if __name__ == '__main__':
    print(get_id_from_name("fire rune"))
