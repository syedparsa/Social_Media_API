
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint



class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass
class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True

class Userlogin(BaseModel):
    email: EmailStr
    password: str

class UserloginREsponse(BaseModel):
    email: EmailStr
class PostBase (BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

class PostCreate(PostBase):
       pass

class PostResponse(PostBase):
    id:int
    owner_id: int
    created_at: datetime
    owner_info: UserResponse
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    post: PostResponse
    votes: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
        id: Optional[str] = None

class VotesBase(BaseModel):
    post_id: int
    direction: conint(le=1)