from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.db.database import SessionLocal, engine
from app.utils.hashing import Hasher
from sqlalchemy.orm import Session

from app.models import user
from app.schemas import users
from app.crud import crud
from jose import JWTError, jwt

SECRET_KEY = "6bf11ba31884f6136eb2025676851c2a9625e0e79d4629eb6f37587a2e66accb"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

user.Base.metadata.create_all(bind=engine)

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

@router.post("/login/{sns_type}", status_code=200)
async def login(sns_type: users.SnsType, user_info: users.UserRegister, db: Session = Depends(get_db)):
    if sns_type == sns_type.email:
        is_exist = crud.get_user(db, user_info.email)

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

@router.post("/register/{sns_type}", status_code=200)
async def register(sns_type: users.SnsType, user_info: users.UserRegister, db: Session = Depends(get_db)):
    if sns_type == sns_type.email:
        email = user_info.email
        password = user_info.password

        if not user_info.email or not user_info.password or not user_info.full_name:
                return JSONResponse(status_code=400, content=dict(detail="Email, PW and Full Name must be provided'"))

        is_exist = crud.get_user(db, email)

        if is_exist:
            return JSONResponse(
                content=dict(message='already signed up'),
                status_code=400
            )
        pw_hashed = Hasher.get_password_hash(password.encode('utf-8'))
        crud.create_user(db, user_info.id, user_info.email, pw_hashed, user_info.full_name, sns_type)
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
        data={"sub": user_info.full_name}, expires_delta=access_token_expires
    )
        return JSONResponse(status_code=200, content=dict({"access_token": access_token, "token_type": "bearer"}))
    else:
        return JSONResponse(status_code=400, content=dict(detail="UNSUPPORTED"))




    


