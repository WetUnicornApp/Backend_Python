from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base
from app.models.base import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String(100), default='')
    last_name = Column(String(100), default='')
    email = Column(String(255), unique=True)
    password = Column(String(255), default='')



