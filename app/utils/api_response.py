from flask import jsonify
from dataclasses import dataclass
from typing import Any, Union, List
from pydantic import BaseModel

@dataclass
class ApiResponse:
    message: str
    success: bool
    data: Union[BaseModel, dict, str, None, List[Union[BaseModel, dict, str]]] = None

    def return_response(self):
        response_data = {
            "message": self.message,
            "success": self.success,
            "data": self._serialize_data()
        }
        return jsonify(response_data)

    def _serialize_data(self) -> Any:
        if isinstance(self.data, list):
            return [item.dict() if isinstance(item, BaseModel) else item for item in self.data]
        if isinstance(self.data, BaseModel):
            return self.data.dict()
        return self.data
