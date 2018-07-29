from get_config import get_config
from bs4 import BeautifulSoup
import py_logging
import requests
import urllib
import os


def get_id_from_name(name: str, setting: str = 'DEFAULT') -> int:
    logger = py_logging.create_logger(
        'get_id_from_name', '{}get_id_from_name.log'.format(os.path.dirname(os.path.realpath(__file__)) + os.sep))
    config = get_config()

    html_text = requests.get(
        config[setting]['NameToIdBaseUrl'] +
        urllib.parse.quote_plus(name)).text
    logger.info("Sent request off to find the id for: {}".format(name))

    soup = BeautifulSoup(html_text, 'html.parser')

    possible_results = soup.find('table', {"class": "table"}) \
                           .find_all('tr')

    for possible_result in possible_results:
        holder = possible_result.find_all('td')
        possible_result = possible_result.find('td')
        if holder:
            if len(holder) > 1:
                holder = holder[1]
                if holder.getText().lower() == name.lower():
                    return possible_result.getText()

    return None


if __name__ == '__main__':
    pass
