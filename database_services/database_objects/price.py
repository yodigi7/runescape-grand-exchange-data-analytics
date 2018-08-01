from sqlalchemy import Column, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import Session, relationship
import multiprocessing

from database_services.database.base import Base
from database_services.session_controller import shared_session


def add_all_to_database(list_of_prices: list, lock: multiprocessing.Lock) -> None:
    with lock:
        session = shared_session()
        session.add_all(list_of_prices)
        session.commit()
        session.close()


class Price(Base):
    __tablename__ = 'prices'

    item_id = Column(Integer, ForeignKey("items.item_id"), primary_key=True)
    runescape_time = Column(BigInteger, primary_key=True)
    price = Column(BigInteger)

    item = relationship("Item", back_populates="prices")

    def get_from_database(self, lock: multiprocessing.Lock):
        with lock:
            session = shared_session()
            return session.query(Price).filter_by(item_id=self.item_id).first()

    def add_to_database(self, lock: multiprocessing.Lock) -> None:
        with lock:
            session = shared_session()
            session.add(self)
            session.commit()
            session.close()

    def delete_in_database(self, lock: multiprocessing.Lock) -> None:
        with lock:
            session = shared_session()
            session.delete(session.query(Price).filter_by(item_id=self.item_id).first())
            session.commit()
            session.close()

    def update_in_database(self, lock: multiprocessing.Lock) -> None:
        with lock:
            session = shared_session()
            session.delete(session.query(Price).filter_by(item_id=self.item_id).first())
            session.add(self)
            session.commit()
            session.close()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Price(item_id = {}, runescape_time={}, price={})' \
            .format(self.item_id, self.runescape_time, self.price)


if __name__ == '__main__':
    pass
