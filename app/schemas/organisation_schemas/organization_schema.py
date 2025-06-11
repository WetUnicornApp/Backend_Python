from app.schemas.schema import Schema


class OrganizationSchema(Schema):
    name: str = ''
    address: str = ''