from typing import TypeVar, Type

from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound="Schema")


class Schema(BaseModel):
    @classmethod
    def convert_to_schema(cls: Type[T], data: dict) -> T:
        """
        Generic method to convert a dictionary to a schema
        """
        try:
            return cls(**data)
        except ValidationError as e:
            raise ValueError(f"Invalid data for {cls.__name__}: {e}")
