from datetime import datetime, timedelta
import json
from typing import Any, Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db.database import SessionLocal, engine
from app.utils.hashing import Hasher
from sqlalchemy.orm import Session

from pytz import timezone

from app.models import models 
from app.schemas import item, users
from app.crud import crud
from jose import JWTError, jwt

SECRET_KEY = "6bf11ba31884f6136eb2025676851c2a9625e0e79d4629eb6f37587a2e66accb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

models.Base.metadata.create_all(bind=engine)

router = APIRouter()
        
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create", status_code=200)
async def create(item_info: item.ItemCreate, db: Session = Depends(get_db)):
    if not item_info.title or not item_info.description:
        return JSONResponse(status_code=400, content=dict(detail="Title and descriptionription must be provided'"))
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
    if not item_info.title or not item_info.description:
        return JSONResponse(status_code=400, content=dict(detail="Title and description must be provided'"))

    crud.get_item(db, item_info.id)
    return JSONResponse(status_code=200, content=dict({"title": item_info.title, "description": item_info.description, "created_at": "UNKNOWN"}))