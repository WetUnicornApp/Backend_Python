
from datetime import datetime, date


from sqlalchemy import Column, DateTime

from app.models.calendar_models.calendar_model import CalendarModel


class Calendar(CalendarModel):
    __tablename__ = "calendar"
    datetime_created = Column(DateTime, default=datetime)
    datetime_planned = Column(DateTime, default=datetime)
    def to_dict(self):
        return {
            "datetime_created": self.datetime_created,
            "datetime_planned": self.datetime_planned,
        }

