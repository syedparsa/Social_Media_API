import time
from typing import Optional
from fastapi import Body, FastAPI, Response , status , HTTPException
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
app = FastAPI()


class POST(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

while True:
    try:
        connection = psycopg2.connect(host = 'localhost', database = 'social_media_api_db',
                                  user = 'postgres', password= 'syed', cursor_factory=RealDictCursor )
        cursor = connection.cursor()
        print('Datebase connection was successful')
        break
    except Exception as error:
        print('connection to the database failed')
        print('Errot:',error)
        time.sleep(5)



my_post_storage = [{'title':'this is title one ', 'content':'this is the content', 'id':1}]


def find_post_by_id (id):
    for post in my_post_storage:
        if post['id'] == id:
            return post



def find_post_index(id):
    for index,post in enumerate(my_post_storage):
        if post['id'] == id:
             return index


@app.get("/")
def read_root():
    #return {"Whats up boi": "Welcome to my social_media_api"}
    print(my_post_storage)

@app.get('/posts')
def get_posts():

    cursor.execute(""" SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {'All_Posts': posts}


@app.post('/posts', status_code=status.HTTP_201_CREATED)
def create_post(post: POST):
# using the PGDB to store the data
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES(%s, %s, %s) returning * """,(post.title, post.content,post.published))
    new_post = cursor.fetchone()
    connection.commit()


    return {'new_post': new_post}


# Using internal memory (list/dict) to store data locally
    # post_dict = post.model_dump()
    # post_dict['id'] = randrange(0,1000000)
    # my_post_storage.append(post_dict)
    # return f'newpost:{post_dict}'


@app.get('/posts/latest')
def get_latest_post():
    post = my_post_storage[len(my_post_storage)-1]
    return {'lates_post':post}


@app.get('/posts/{id}')
def get_post(id: int, response: Response):


    cursor.execute("""SELECT * FROM posts WHERE id = %s   """,(str(id)))
    post = cursor.fetchone()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id:{id} does not exists')
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'error':f"Post with {id} does not exist."}
    return {'post_details':post}

@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):


    cursor.execute(""" DELETE FROM posts WHERE id = %s returning * """ , (str(id),))
    deleted_post = cursor.fetchone()
    connection.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id:{id} does not contain any associated post in  the system')

    return {'deleted_post':deleted_post}

@app.put('/posts/{id}')
def update_post(id:int, post:POST ):

    cursor.execute("""UPDATE posts SET title = %s , content = %s , published =%s  WHERE id = %s RETURNING *""",(post.title, post.content, post.published,str(id)))
    update_post = cursor.fetchone()
    connection.commit()



    if update_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id:{id} not found")

    return {'update':update_post}