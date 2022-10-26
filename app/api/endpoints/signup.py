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


@router.post("/signup/{sns_type}", status_code=200)
async def signup(sns_type: users.SnsType, user_info: users.UserSignup, db: Session = Depends(get_db)):
    if sns_type == sns_type.email:

        if not user_info.email or not user_info.password or not user_info.full_name:
                return JSONResponse(status_code=400, content=dict(detail="Email, PW and Full Name must be provided'"))

        is_exist = crud.get_user(db, id)

        if is_exist:
            return JSONResponse(
                content=dict(message='already signed up'),
                status_code=400
            )
        pw_hashed = Hasher.get_password_hash(user_info.password.encode('utf-8'))
        crud.create_user(db, user_info.id, user_info.email, pw_hashed, user_info.full_name, sns_type)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
        data={"sub": user_info.full_name}, expires_delta=access_token_expires
    )
        return JSONResponse(status_code=200, content=dict({"access_token": access_token, "token_type": "bearer"}))
    else:
        return JSONResponse(status_code=400, content=dict(detail="UNSUPPORTED"))

