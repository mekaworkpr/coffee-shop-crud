from sqlalchemy import Column, Integer

from coffee_shop.sqlalchemy_db.base import Base


class Test(Base):
    __tablename__ = 'test'

    id = Column(Integer, primary_key=True)