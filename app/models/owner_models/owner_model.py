from dataclasses import dataclass

from app.models.model import Model



class OwnerModel(Model):
    """base class for objects from this directory"""
    __abstract__ = True
    pass
