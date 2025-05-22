from datetime import datetime
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, DateTime, Boolean, String

Base = declarative_base()


class Model(Base):
    __abstract__ = True

    id = Column(Integer, primary_key=True, autoincrement=True)
    datetime_created = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    identifier = Column(String(32), unique=True, nullable=False)

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.id == other.id
        return False

    def __hash__(self):
        return hash(self.id)
