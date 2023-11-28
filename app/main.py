
from fastapi import  FastAPI
from .database import  engine, get_db
from . import models
from .routers import post,users, auth




models.Base.metadata.create_all(bind=engine)
app = FastAPI()



app.include_router(post.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
def read_root():
    return {"Whats up boi": "Welcome to my social_media_api"}

