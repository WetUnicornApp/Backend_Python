from app.schemas.schema import Schema


class VisitSchema(Schema):
    name : str = ''
    description : str = ''
    calendar_id : int
