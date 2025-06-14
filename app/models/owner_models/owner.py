
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.models.owner_models.owner_model import OwnerModel


class Owner(OwnerModel):
    __tablename__ = "owner"
    user_id: int = Column(Integer, ForeignKey("users.id"))
    user = relationship("User", back_populates="owners")
    animals = relationship("Animal", back_populates="owner")
    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id
        }
    pass