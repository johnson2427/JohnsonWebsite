from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from odmantic import AIOEngine, Model
from pydantic import BaseModel

ModelType = TypeVar("ModelType", bound=Model)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        **Parameters**

        * `model`: A Mongo model class
        * `schema`: A Pydantic model (schema) class
        """
        self.model = model

    async def get(self, db: AIOEngine, id: Any) -> Optional[ModelType]:
        if (db_obj := await db.find_one(self.model, {"id": id})) is not None:
            return db_obj  # type: ignore
        return None

    async def get_multi(
        self, db: AIOEngine, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        return await db.find(self.model, limit=limit, skip=skip)  # type: ignore

    async def create(self, db: AIOEngine, *, obj_in: CreateSchemaType) -> ModelType:
        db_obj = self.model(**jsonable_encoder(obj_in))  # type: ignore
        await db.save(db_obj)  # type: ignore
        return db_obj  # type: ignore

    async def update(
        self,
        db: AIOEngine,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]],
    ) -> ModelType:
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        await db.save(db_obj)
        return db_obj

    async def remove(self, db: AIOEngine, *, id: int) -> ModelType:
        q = await db.find_one(self.model, {"_id": id})
        await db.delete(q)  # type: ignore
        return q  # type: ignore
