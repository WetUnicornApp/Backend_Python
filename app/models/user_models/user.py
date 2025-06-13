from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.orm import relationship

from app.models.model import Model
from app.models.user_models.user_model import UserModel


class User(UserModel):
    __tablename__ = 'users'

    first_name = Column(String(100), default='')
    last_name = Column(String(100), default='')
    email = Column(String(255), unique=True)
    password = Column(String(255), default='')

    owners = relationship("Owner", back_populates="user")
    employees = relationship("Employee", back_populates="user")


    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
        }
