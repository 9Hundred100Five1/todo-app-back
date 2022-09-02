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

def create_user(db: Session, users: users.UserRegister):
    hashed_password = Hasher.get_password_hash(users.password)
    db_user = user.User(email=users.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user