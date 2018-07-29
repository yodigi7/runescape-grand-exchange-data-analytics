from sqlalchemy import Column, Integer, String, Boolean, create_engine
from sqlalchemy.orm import Session, relationship, sessionmaker

from database_services.database.base import Base

import threading
import time

from get_config import get_config


class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(String(100))
    is_members_only = Column(Boolean)
    description = Column(String(1000))

    prices = relationship("Price", back_populates="item")

    def get_from_database(self, session: Session):
        return session.query(Item).filter_by(item_id=self.item_id).first()

    def add_to_database(self, session: Session) -> None:
        session.add(self)
        session.commit()

    def delete_in_database(self, session: Session) -> None:
        session.delete(session.query(Item).filter_by(item_id=self.item_id).first())
        session.commit()

    def update_in_database(self, session: Session) -> None:
        session.delete(session.query(Item).filter_by(item_id=self.item_id).first())
        session.add(self)
        session.commit()

    def add_to_database_thread(self, lock: threading.Lock) -> None:
        print(threading.get_ident())
        config = get_config()
        engine = create_engine(
            '{}:///{}{}'.format(
                config['DEFAULT']['DatabaseType'], "C:\\Anthony\\Programs\\runescape-grand-exchange-data-analytics\\database_services\\database\\", config['DEFAULT']['DatabaseName']))
        Session = sessionmaker(bind=engine)
        with lock:
            session = Session()
            session.add(self)
            session.commit()
            session.close()

    def delete_in_database_thread(self, session: Session, lock: threading.Lock) -> None:
        with lock:
            session.delete(session.query(Item).filter_by(item_id=self.item_id).first())
            session.commit()

    def update_in_database_thread(self, session: Session, lock: threading.Lock) -> None:
        with lock:
            session.delete(session.query(Item).filter_by(item_id=self.item_id).first())
            session.add(self)
            session.commit()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Item(item_id = {}, name="{}", type="{}", is_members_only={}, description="{}")' \
            .format(self.item_id, self.name, self.type, self.is_members_only, self.description)


if __name__ == '__main__':
    pass
