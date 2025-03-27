import enum

from sqlalchemy import Column, Integer, Float, ForeignKey, DateTime, Enum, func

from coffee_shop.sqlalchemy_db.base import Base


class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING, nullable=False)
    total_price = Column(Float, nullable=False)
