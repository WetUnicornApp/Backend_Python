from sqlalchemy import Column, Integer, String, create_engine
from app.models.model import Model


class User(Model):
    __tablename__ = 'users'

    first_name = Column(String(100), default='')
    last_name = Column(String(100), default='')
    email = Column(String(255), unique=True)
    password = Column(String(255), default='')



