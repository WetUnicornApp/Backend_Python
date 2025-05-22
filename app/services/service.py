from typing import Type, TypeVar, Generic
from pydantic import ValidationError

from app.repositories.repository import Repository
from app.schemas.schema import Schema
from app.utils.api_response import ApiResponse

ModelT = TypeVar("ModelT")
SchemaT = TypeVar("SchemaT", bound=Schema)
RepoT = TypeVar("RepoT", bound=Repository)


class Service(Generic[ModelT, SchemaT, RepoT]):
    def __init__(self, model_cls: Type[ModelT], schema_cls: Type[SchemaT], repo_cls: Type[RepoT]):
        self.model_cls = model_cls
        self.schema_cls = schema_cls
        self.repo_cls = repo_cls

    def create(self, json_data: dict, db_session) -> ApiResponse:
        try:
            schema_obj = self.schema_cls.parse_obj(json_data)

            # 2. Mapowanie Schema → Model
            model_obj = self._schema_to_model(schema_obj)

            repo = self.repo_cls.instance(db_session)
            return repo.create(model_obj)

        except ValidationError as e:
            return ApiResponse("Validation error", False, e.errors())
        except Exception as e:
            return ApiResponse("Error while creating object", False, str(e))

    def _schema_to_model(self, schema_obj: SchemaT) -> ModelT:
        if hasattr(schema_obj, "to_model"):
            return schema_obj.to_model()

        model_fields = {c.name for c in self.model_cls.__table__.columns}
        filtered_data = {
            key: value for key, value in schema_obj.dict().items()
            if key in model_fields
        }
        return self.model_cls(**filtered_data)
