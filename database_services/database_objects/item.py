from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, relationship

from database_services.database.base import Base


class Item(Base):
    __tablename__ = 'items'

    item_id = Column(Integer, primary_key=True)
    name = Column(String(100))
    type = Column(String(100))
    description = Column(String(1000))

    prices = relationship("Price", back_populates="item")

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


if __name__ == '__main__':
    pass
