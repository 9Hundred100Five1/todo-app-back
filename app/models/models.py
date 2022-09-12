from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, primary_key=True, unique=True, index=True, nullable=False)
    password= Column(String, primary_key=True, nullable=False)
    full_name=Column(String, primary_key=True, nullable=False)
    sns_type = Column(String, primary_key=True, index=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, primary_key=True, index=True)
    description = Column(String, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")