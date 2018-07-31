from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from get_config import get_config


config = get_config()
engine = create_engine(
    '{}:///{}{}'.format(
        config['DEFAULT']['DatabaseType'], "C:\\Anthony\\Programs\\runescape-grand-exchange-data-analytics\\database_services\\database\\", config['DEFAULT']['DatabaseName']))
shared_session = sessionmaker(bind=engine)

