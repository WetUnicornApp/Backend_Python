from dataclasses import dataclass, field
from datetime import datetime
import uuid

from app.models.model import Model


@dataclass
class AnimalModel(Model):
    """base class for objects from this directory"""
    pass