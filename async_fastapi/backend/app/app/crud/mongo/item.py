from app.crud.mongo.base import CRUDBase
from app.models.mongo.item import Items
from app.schemas.mongo.item import CreateItemsModel, UpdateItemsModel


class CRUDMongoItem(CRUDBase[Items, CreateItemsModel, UpdateItemsModel]):
    """
    Item CRUD class.
    """


mongo_item_crud = CRUDMongoItem(Items)
