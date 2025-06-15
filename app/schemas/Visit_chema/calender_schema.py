

from flask_restful import fields

from app.schemas.schema import Schema
from datetime import datetime

class CalenderSchema(Schema):
    datetime_created : datetime
    datetime_planned : datetime