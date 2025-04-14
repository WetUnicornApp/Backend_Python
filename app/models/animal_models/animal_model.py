from dataclasses import dataclass, field
from datetime import datetime
import uuid

from Backend_Python.app.models.model import Model


@dataclass
class AnimalModel(Model):
    """base class for objects from this directory"""
    pass