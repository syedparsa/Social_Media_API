
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr

class PostBase (BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class PostCreate(PostBase):
       pass

class PostResponse(PostBase):
    id:int
    created_at: datetime
    class Config:
        orm_mode = True




class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    email: EmailStr
    class Config:
        orm_mode = True