from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from psycopg_pool import ConnectionPool
from .db.models import Base
from .db.database import engine, SessionLocal

Base.metadata.create_all(bind=engine)

app = FastAPI()

DATABASE_URL = "host=localhost dbname=fastapi user=postgres password=1298"

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

try:
    pool = ConnectionPool(conninfo=DATABASE_URL)
except Exception as e:
    print("Error connecting to database")
    print(e)

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}

@app.get("/posts")
def get_posts():
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            posts = cursor.execute("SELECT * FROM posts").fetchall()
    return {"posts": posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """INSERT INTO posts (title, content, published)
                VALUES (%s, %s, %s)
                RETURNING *;""", 
                (post.title, post.content, post.published)
            )
        conn.commit()
        return { "new_post": cursor.fetchone()}

@app.get("/posts/{id}")
def get_post(id: int):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """SELECT * 
                FROM posts
                WHERE id = %s;""",
                (id,)
            )
            post = cursor.fetchone()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Can't find a post with ID {id}")
        return {"post": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """DELETE FROM posts
                WHERE id=%s
                RETURNING *;""",
                (id,)
            )
            post_to_delete = cursor.fetchone()
            if not post_to_delete:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Post with ID '{id}' not found")

            return

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED)
def update_post(id: int, post: Post):
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(
                """UPDATE posts
                SET title=%s, content=%s, published=%s
                WHERE id=%s
                RETURNING *;""",
                (post.title, post.content, post.published, id)
            )
            updated_post = cursor.fetchone()
            if not updated_post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                    detail=f"Post with ID '{id}' not found")
            conn.commit()
            
            return {"data" : updated_post}