from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    id : Optional[int]
    owner_id: int

    class Config:
        orm_mode = True

class ItemCreate(ItemBase):
    pass

class ItemDelete(BaseModel):
    id: int
    
    class Config:
        orm_mode = True

class ItemUpdate(ItemBase):
    pass



