from flask import jsonify
from dataclasses import dataclass, asdict
from typing import Any, Union
from pydantic import BaseModel
@dataclass
class ApiResponse:
    message: str
    success: bool
    data: Union[dict, str, None, BaseModel] = None

    def return_response(self):
        response_data = {
            "message": self.message,
            "success": self.success,
            "data": self._serialize_data()
        }
        return jsonify(response_data)

    def _serialize_data(self) -> Any:
        # Obsługa obiektów Pydantic (np. z .dict()), słowników, lub None
        if hasattr(self.data, "dict"):
            return self.data.dict()
        return self.data
