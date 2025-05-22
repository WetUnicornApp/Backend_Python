from flask import jsonify
from dataclasses import dataclass
from typing import Any, Union, List
from pydantic import BaseModel

@dataclass
class ApiResponse:
    message: str
    success: bool
    data: Union[BaseModel, dict, str, None, List[Union[BaseModel, dict, str, Any]]] = None

    def return_response(self):
        response_data = {
            "message": self.message,
            "success": self.success,
            "data": self._serialize_data()
        }
        return jsonify(response_data)

    def _serialize_data(self) -> Any:
        if isinstance(self.data, list):
            return [self._serialize_item(item) for item in self.data]
        return self._serialize_item(self.data)

    def _serialize_item(self, item: Any) -> Any:
        if isinstance(item, BaseModel):
            return item.dict()
        if hasattr(item, "to_dict") and callable(item.to_dict):
            return item.to_dict()
        if isinstance(item, dict) or isinstance(item, str) or item is None:
            return item
        return str(item)  # fallback
