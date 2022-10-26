from sqlalchemy.orm import Session

from app import schemas
from app.models.models import Item, User
from app.schemas import users
from app.schemas import item
from app.utils.authenticate import Hasher


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(User).offset(skip).limit(limit).all()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Item).offset(skip).limit(limit).all()


def create_item(db: Session, item: item.ItemCreate):
    db_item = Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_user(db: Session, user_id: int):
    if db.query(User).filter(User.id == user_id).first():
        return db.query(User).filter(User.id == user_id).first()
    else:
        return None

def del_item(db: Session, item_id: int):
    session = db.query(Item).filter_by(id=item_id)
    session.delete()
    db.commit()

def get_item(db: Session, item_id: int):
    if db.query(Item).filter(Item.id == item_id).first():
        return db.query(Item).filter(Item.id == item_id).first()
    else:
        return None

def create_user(db: Session, user_id:int, user_email: str, user_password: str, user_full_name: str, sns_type:str):
    hashed_password = Hasher.get_password_hash(user_password)
    db_user = User(id=user_id, email=user_email, full_name=user_full_name, password=hashed_password, sns_type=sns_type)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
