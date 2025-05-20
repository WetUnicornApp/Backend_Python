from dataclasses import field
from datetime import datetime

from attr import dataclass

from app.models.calendar_models.calendar_model import CalendarModel


@dataclass
class Calendar(CalendarModel):
    """
    collective class for time organization
    """
    datetime_created: datetime = field(default=datetime.now())
    datetime_planned: datetime = field(default=datetime.now())
