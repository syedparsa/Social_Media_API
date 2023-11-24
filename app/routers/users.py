
from typing import List

from fastapi import Depends, FastAPI, Response, status , HTTPException,APIRouter
from sqlalchemy.orm import Session
from app.database import  engine, get_db
from app import models, schemas, utils

router = APIRouter(
    prefix='/users',
    tags=['Users']
)

# CRUD Operation for the user

@router.get('/', response_model= List [schemas.UserResponse])
def get_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post('/',status_code=status.HTTP_201_CREATED,response_model= schemas.UserResponse)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
# usign ORM to create a new post in the DB using sqlalchemy

    hashed_passwd = utils.hash(user.password)
    user.password = hashed_passwd
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',status_code=status.HTTP_201_CREATED,response_model= schemas.UserResponse)
def get_user_by_id(id:int, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == str(id)).first()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id:{id} does not exists')

    return user_query

@router.delete('/{id}')
def delete_user(id:int,db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.id == id )
    if user_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user associated with id:{id} does not exists')
    user_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# @router.put('/{id}',response_model= schemas.UserResponse)
# def update_user(id:int, user = schemas.UserBase, db: Session = Depends(get_db)):
#     user_query = db.query(models.User).filter(models.User.id == id )
#     update_user = user_query.first()
#     if update_user == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'user associated with id:{id} does not exists')
#     user_query.update(user.model_dump())
#     db.commit()
#     return user_query.first()