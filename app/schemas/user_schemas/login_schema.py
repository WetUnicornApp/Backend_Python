from app.schemas.schema import Schema


class LoginSchema(Schema):
    email: str = ''
    password: str = ''
