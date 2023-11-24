
from typing import List

from fastapi import Depends, FastAPI, Response, status , HTTPException, APIRouter
from sqlalchemy.orm import Session
from app.database import  engine, get_db
from app import models, schemas


router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)




@router.get('/', response_model= List [schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    post =  db.query(models.Post).all()
    return post


    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return {'All_Posts': posts}


@router.post('/', status_code=status.HTTP_201_CREATED,response_model= schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
# usign ORM to create a new post in the DB using sqlalchemy


    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

#using the PGDB to store the data
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) returning * """,(post.title, post.content,post.published))
    # new_post = cursor.fetchone()
    # connection.commit()

# Using internal memory (list/dict) to store data locally
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(0,1000000)
    # my_post_storage.append(post_dict)
    # return f'newpost:{post_dict}'


# @app.get('/posts/latest')
# def get_latest_post():
#     post = my_post_storage[len(my_post_storage)-1]
#     return {'lates_post':post}


@router.get('/{id}', response_model= schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
# Updated code using ORM instead if direct db server

    post_by_id = db.query(models.Post).filter(models.Post.id == str(id)).first()
    if not post_by_id:
        raise HTTPException(status_code=404, detail=f'Post with id:{id} not found')
    return  post_by_id


    # cursor.execute("""SELECT * FROM posts WHERE id = %s   """,(str(id)))
    # post = cursor.fetchone()

    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} does not exists')
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {'error':f"Post with {id} does not exist."}
    # return {'post_details':post}

@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
# Updated code using ORM instead if direct db server

    post = db.query(models.Post).filter(models.Post.id == id)
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id:{id} does not have associated post to it')
    post.delete()
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)

    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """ , (str(id),))
    # deleted_post = cursor.fetchone()
    # connection.commit()
    # if deleted_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id:{id} does not contain any associated post in  the system')

    # return {'deleted_post':deleted_post}

@router.put('/{id}', response_model= schemas.PostResponse)
def update_post(id:int, post:schemas.PostBase, db: Session = Depends (get_db) ):
#   Updated code using ORM instead if direct db server

    post_query = db.query(models.Post).filter(models.Post.id == id )
    update_post  = post_query.first()

    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id:{id} does not exists')
    post_query.update(post.model_dump())

    db.commit()

    # cursor.execute("""UPDATE posts SET title = %s , content = %s , published =%s  WHERE id = %s RETURNING *""",(post.title, post.content, post.published,str(id)))
    # update_post = cursor.fetchone()
    # connection.commit()
    # if update_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")

    return post_query.first()