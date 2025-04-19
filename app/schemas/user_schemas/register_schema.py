from Backend_Python.app.schemas.schema import Schema


class RegisterSchema(Schema):
    first_name: str = ''
    last_name: str = ''
    email: str = ''
    password: str = ''
    repeat_password: str = ''