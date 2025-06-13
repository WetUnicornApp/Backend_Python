from dataclasses import dataclass, field
from datetime import datetime
import uuid

from app.models.model import Model



class AnimalModel(Model):
    """base class for objects from this directory"""
    __abstract__ = True
    pass