
from typing import List
from fastapi import Depends, FastAPI, Response, status , HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .database import  engine, get_db
from . import models, schemas, utils
from .routers import post,users




models.Base.metadata.create_all(bind=engine)
app = FastAPI()



app.include_router(post.router)
app.include_router(users.router)

@app.get("/")
def read_root():
    return {"Whats up boi": "Welcome to my social_media_api"}

