from typing import List

from fastapi import APIRouter, HTTPException
from odmantic import AIOEngine

from app.crud.mongo.item import mongo_item_crud
from app.db.mongo.session import mongo_client
from app.models.mongo.item import Items
from app.schemas.mongo.item import CreateItemsModel, UpdateItemsModel

router = APIRouter()
engine = AIOEngine(motor_client=mongo_client, database="Items")


@router.post("/", response_description="Add new item", response_model=Items)
async def create_item(item: CreateItemsModel) -> Items:
    return await mongo_item_crud.create(db=engine, obj_in=item)


@router.get("/{id}", response_description="Get an item by ID", response_model=Items)
async def get_item_by_id(id: int) -> Items:
    item = await mongo_item_crud.get(engine, id)
    if item:
        return item

    raise HTTPException(status_code=404, detail=f"Item ID {id} not found")


@router.get("/{name}", response_description="Get a single item", response_model=Items)
async def get_item(name: str) -> Items:
    if (item := await engine.find_one(Items, {"name": name})) is not None:
        return item

    raise HTTPException(status_code=404, detail=f"Item {name} not found")


@router.get("/", response_description="List all items", response_model=List[Items])
async def list_items(skip: int = 0, limit: int = 100) -> List[Items]:
    return await mongo_item_crud.get_multi(db=engine, skip=skip, limit=limit)


@router.put("/{name}", response_description="Update an item", response_model=Items)
async def update_item(name: str, patch: UpdateItemsModel) -> Items:
    item = await engine.find_one(Items, Items.name == name)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {name} not found")
    return await mongo_item_crud.update(db=engine, db_obj=item, obj_in=patch)


@router.delete("/{name}", response_description="Delete an item")
async def delete_item(name: str) -> str:
    item = await engine.find_one(Items, Items.name == name)
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {name} not found")
    return await mongo_item_crud.remove(db=engine, id=item.id)  # type: ignore
