from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db.database import  engine, get_db
from app.utils.authenticate import Hasher, create_access_token
from sqlalchemy.orm import Session

from app.models import models
from app.schemas import users
from app.crud import crud

ACCESS_TOKEN_EXPIRE_MINUTES = 30


router = APIRouter()

@router.post("/signin/{sns_type}", status_code=200)
async def signin(sns_type: users.SnsType, user_info: users.UserSignup, db: Session = Depends(get_db)):
    if sns_type == sns_type.email:
        is_exist = crud.get_user(db, user_info.id)

        if not user_info.email or not user_info.password or not user_info.full_name:
            return JSONResponse(status_code=400, content=dict(detail="Email, PW and Full Name must be provided'"))

        if not is_exist:
            return JSONResponse(status_code=400, content=dict(detail="NO_MATCH_USER"))
        pw_hashed = Hasher.get_password_hash(user_info.password)
        is_verified = Hasher.verify_password(user_info.password, pw_hashed)

        if not is_verified:
            return JSONResponse(status_code=400, content=dict(detail="NO_MATCH_USER"))

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
        data={"sub": user_info.full_name}, expires_delta=access_token_expires
    )
        return JSONResponse(status_code=200, content=dict({"access_token": access_token, "token_type": "bearer"}))
    else:
        return JSONResponse(status_code=400, content=dict(detail="UNSUPPORTED"))


