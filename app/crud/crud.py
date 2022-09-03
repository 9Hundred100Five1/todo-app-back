from sqlalchemy.orm import Session

from app import schemas
from app.models import user
from app.schemas import users
from app.schemas import item
from app.utils.hashing import Hasher


def get_user_by_email(db: Session, email: str):
    return db.query(user.User).filter(user.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user.User).offset(skip).limit(limit).all()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(user.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: item.ItemCreate, user_id: int):
    db_item = user.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user(db: Session, user_id: int):
    if db.query(user.User).filter(user.User.id == user_id).first():
        return db.query(user.User).filter(user.User.id == user_id).first()
    else:
        return None

def create_user(db: Session, user_id:int, user_email: str, user_password: str, user_full_name: str, sns_type:str):
    hashed_password = Hasher.get_password_hash(user_password)
    db_user = user.User(id=user_id, email=user_email, full_name=user_full_name, password=hashed_password, sns_type=sns_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
