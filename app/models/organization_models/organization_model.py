from dataclasses import dataclass

from sqlalchemy import Column, Integer,String

from app.models.model import Model

@dataclass
class OrganizationModel(Model):
    __tablename__ = 'organization'
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
        }

    pass
