from bson import ObjectId
from pydantic import BaseModel


class CreateItemsModel(BaseModel):
    name: str
    date: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {"example": {"name": "async-fastapi", "date": "2022-11-19"}}


class UpdateItemsModel(BaseModel):
    name: str
    date: str

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {"example": {"name": "async-fastapi", "date": "2022-11-19"}}
