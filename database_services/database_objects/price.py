from sqlalchemy import Column, Integer, BigInteger, ForeignKey
from sqlalchemy.orm import Session, relationship

from database_services.database.base import Base


class Price(Base):
    __tablename__ = 'prices'

    item_id = Column(Integer, ForeignKey("items.item_id"), primary_key=True)
    runescape_time = Column(BigInteger, primary_key=True)
    price = Column(BigInteger)

    item = relationship("Item", back_populates="prices")

    def get_from_database(self, session) -> Session:
        return session.query(Price).filter_by(item_id=self.item_id).first()

    def add_to_database(self, session) -> None:
        session.add(self)
        session.commit()

    def delete_in_database(self, session) -> None:
        session.delete(session.query(Price).filter_by(item_id=self.item_id).first())
        session.commit()

    def update_in_database(self, session) -> None:
        session.delete(session.query(Price).filter_by(item_id=self.item_id).first())
        session.add(self)
        session.commit()

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return 'Price(item_id = {}, name="{}", type="{}", description="{}")' \
            .format(self.item_id, self.name, self.type, self.description)


if __name__ == '__main__':
    pass
