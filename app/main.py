import json
import time

from fastapi import Body, Depends, FastAPI, Response, status , HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from .database import  engine, get_db
from . import models, schemas



models.Base.metadata.create_all(bind=engine)
app = FastAPI()



# while True:
#     try:
#         connection = psycopg2.connect(host = 'localhost', database = 'social_media_api_db',
#                                   user = 'username', password= 'password', cursor_factory=RealDictCursor )
#         cursor = connection.cursor()
#         print('Datebase connection was successful')
#         break
#     except Exception as error:
#         print('connection to the database failed')
#         print('Errot:',error)
#         time.sleep(5)



# my_post_storage = [{'title':'this is title one ', 'content':'this is the content', 'id':1}]


# def find_post_by_id (id):
#     for post in my_post_storage:
#         if post['id'] == id:
#             return post



# def find_post_index(id):
#     for index,post in enumerate(my_post_storage):
#         if post['id'] == id:
#              return index





@app.get("/")
def read_root():
    return {"Whats up boi": "Welcome to my social_media_api"}


@app.get('/posts')
def get_posts(db: Session = Depends(get_db)):
    post =  db.query(models.Post).all()
    return {'All_Posts': post}


    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # return {'All_Posts': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
# usign ORM to create a new post in the DB using sqlalchemy


    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

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


@app.get('/posts/{id}')
def get_post(id: int, db: Session = Depends(get_db)):
# Updated code using ORM instead if direct db server

    post_by_id = db.query(models.Post).filter(models.Post.id == str(id)).first()
    if not post_by_id:
        raise HTTPException(status_code=404, detail=f'Post with id:{id} not found')
    return {'Choosen_post': post_by_id}


    # cursor.execute("""SELECT * FROM posts WHERE id = %s   """,(str(id)))
    # post = cursor.fetchone()

    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} does not exists')
    #     # response.status_code = status.HTTP_404_NOT_FOUND
    #     # return {'error':f"Post with {id} does not exist."}
    # return {'post_details':post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
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

@app.put('/posts/{id}')
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

    return {'updated_post': post_query.first()}