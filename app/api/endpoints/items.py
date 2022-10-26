from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db.database import  get_db
from app.utils.authenticate import Hasher
from sqlalchemy.orm import Session


from app.models import models 
from app.schemas import item
from app.crud import crud


ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter()

@router.post("/create", status_code=200)
async def create(item_info: item.ItemCreate, db: Session = Depends(get_db)):
    if not item_info.title:
        return JSONResponse(status_code=400, content=dict(detail="Title and description must be provided'"))

    item_exist = crud.get_item(db, item_info.id)

    if item_exist:
        return JSONResponse(status_code=400, content=dict(detail="Item already exist"))
    crud.create_item(db, item_info)
    return JSONResponse(status_code=200, content=dict({"title": item_info.title, "description": item_info.description}))

@router.delete("/delete", status_code=200)
async def delete(item_info: item.ItemDelete, db: Session = Depends(get_db)):
    if not item_info.id:
        return JSONResponse(status_code=400, content=dict(detail="Item id must be provided'"))
    
    is_exist = crud.get_item(db, item_info.id)

    if not is_exist:
        return JSONResponse(status_code=400, content=dict(detail="NO_MATCH_ITEM"))


    crud.del_item(db, item_info.id)
    return JSONResponse(status_code=200, content=dict(detail="SUCCESS"))

@router.post("/fetch", status_code=200)
async def fetch(item_info: item.ItemCreate, db: Session = Depends(get_db)):
    if not item_info.id:
        crud.get_items(db)
    else:
        crud.get_item(db, item_info.id)
    return JSONResponse(status_code=200, content=dict({"title": item_info.title, "description": item_info.description, "created_at": "UNKNOWN"}))
