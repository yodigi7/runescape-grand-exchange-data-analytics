from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_services.database.base import Base
from database_services.database_objects import item
from database_services.database_objects import price

from get_config import get_config


def create_tables():
    config = get_config()
    engine = create_engine(
        ':///'.join([config['DEFAULT']['DatabaseType'], config['DEFAULT']['DatabaseName']]))
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    create_tables()
