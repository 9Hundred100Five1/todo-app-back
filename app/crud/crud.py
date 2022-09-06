from sqlalchemy.orm import Session

from app import schemas
from app.models import models
from app.schemas import users
from app.schemas import item
from app.utils.hashing import Hasher


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()


def create_user_item(db: Session, item: item.ItemCreate, user_id: int):
    db_item = models.Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user(db: Session, user_id: int):
    if db.query(models.User).filter(models.User.id == user_id).first():
        return db.query(models.User).filter(models.User.id == user_id).first()
    else:
        return None

def del_item(db: Session, item_id: int, owner_id: int):
    return db.delete(models.Item).filter(models.Item.owner_id == owner_id and models.Item.id == item_id).first()

def get_item(db: Session, item_id: int, owner_id: int):
    if db.query(models.Item).filter(models.Item.owner_id == owner_id and models.Item.id == item_id).first():
        return db.query(models.Item).filter(models.Item.owner_id == owner_id and models.Item.id == item_id).first()
    else:
        return None

def create_user(db: Session, user_id:int, user_email: str, user_password: str, user_full_name: str, sns_type:str):
    hashed_password = Hasher.get_password_hash(user_password)
    db_user = models.User(id=user_id, email=user_email, full_name=user_full_name, password=hashed_password, sns_type=sns_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
