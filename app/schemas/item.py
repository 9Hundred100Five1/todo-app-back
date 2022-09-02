from typing import Optional

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: Optional[str]
    desc : Optional[str]
    id : int

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



