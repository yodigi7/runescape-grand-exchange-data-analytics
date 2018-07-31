import threading

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from database_services.database.base import Base
from database_services.session_controller import shared_session


class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(String(100))
    is_members_only = Column(Boolean)
    description = Column(String(1000))

    prices = relationship("Price", back_populates="item")

    def get_from_database(self, lock: threading.Lock = None):
        session = shared_session()
        if lock is not None:
            with lock:
                return session.query(Item).filter_by(item_id=self.item_id).first()
        return session.query(Item).filter_by(item_id=self.item_id).first()

    def add_to_database(self, lock: threading.Lock = None) -> None:
        session = shared_session()
        if lock is not None:
            with lock:
                session.add(self)
                session.commit()
        else:
            session.add(self)
            session.commit()

    def delete_in_database(self, lock: threading.Lock = None) -> None:
        session = shared_session()
        if lock is not None:
            with lock:
                session.delete(session.query(Item).filter_by(item_id=self.item_id).first())
                session.commit()
        else:
            session.delete(session.query(Item).filter_by(item_id=self.item_id).first())
            session.commit()

    def update_in_database(self, lock: threading.Lock = None) -> None:
        session = shared_session()
        if lock is not None:
            with lock:
                session.delete(session.query(Item).filter_by(item_id=self.item_id).first())
                session.add(self)
                session.commit()
        else:
            session.delete(session.query(Item).filter_by(item_id=self.item_id).first())
            session.add(self)
            session.commit()

    def add_to_database_thread(self, lock: threading.Lock) -> None:
        # print(threading.get_ident())
        with lock:
            session = shared_session()
            session.add(self)
            session.commit()
            session.close()

    def delete_in_database_thread(self, lock: threading.Lock) -> None:
        with lock:
            session = shared_session()
            session.delete(session.query(Item).filter_by(item_id=self.item_id).first())
            session.commit()

    def update_in_database_thread(self, lock: threading.Lock) -> None:
        with lock:
            session = shared_session()
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
