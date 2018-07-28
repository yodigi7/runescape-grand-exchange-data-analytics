from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import configparser
import os

Base = declarative_base()


class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(String(100))
    description = Column(String(1000))

    def get_from_database(self, session) -> Session:
        return session.query(Item).filter_by(item_id=self.item_id).first()

    def add_to_database(self, session) -> None:
        session.add(self)
        session.commit()

    def delete_in_database(self, session) -> None:
        session.delete(session.query(Item).filter_by(item_id=self.item_id).first())
        session.commit()

    def update_in_database(self, session) -> None:
        session.delete(session.query(Item).filter_by(item_id=self.item_id).first())
        session.add(self)
        session.commit()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Item(item_id = {}, name="{}", type="{}", description="{}")' \
            .format(self.item_id, self.name, self.type, self.description)


def create_table():
    file = open(os.path.split(os.path.split(os.path.dirname(__file__))[0])[0] + os.sep +'general.config')
    config = configparser.ConfigParser()
    config.read_file(file)
    engine = create_engine('{}:///../database/{}'.format(config['DEFAULT']['DatabaseType'], config['DEFAULT']['DatabaseName']))
    file.close()
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    # Session = sessionmaker()
    # engine = create_engine('sqlite:///../database/runescape-grand-exchange-data.db')
    # session = Session(bind=engine)
    #
    # fire_rune_item = Item(item_id=554,
    #                       name="Fire rune",
    #                       type="Runes, Spells and Teleports",
    #                       description="One of the four basic elemental runes. Used in Magic (13).")
    #
    # fire_rune_item.add_to_database(session)
    # print(fire_rune_item.get_from_database(session).item_id)
    # fire_rune_item.delete_in_database(session)
    create_table()
