import configparser
import os


def get_config() -> configparser.ConfigParser:
    config = configparser.ConfigParser()
    config.read(
        os.path.abspath(os.path.join(os.path.dirname(__file__), 'general.config')))
    return config


if __name__ == '__main__':
    print(get_config())
