from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean

from coffee_shop.sqlalchemy_db.base import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    is_available = Column(Boolean, default=True)
    category_id = Column(Integer, ForeignKey("categories.id"))
