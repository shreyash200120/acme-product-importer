from sqlalchemy import Column, Integer, String, Boolean, Text, Float
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)  # stored lowercase
    name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=True)
    active = Column(Boolean, default=True, nullable=False)


class Webhook(Base):
    __tablename__ = "webhooks"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, nullable=False)
    event_type = Column(String, default="import.completed", nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
