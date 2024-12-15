from typing import List
from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from psycopg_pool import ConnectionPool
from sqlalchemy import select, text, update
from sqlalchemy.orm import Session
from .models import Post, Base
from .database import engine, get_db
from .schemas import PostBase, PostCreate, PostResponse


app = FastAPI()

DATABASE_URL = "host=localhost dbname=fastapi user=postgres password=1298"

try:
    pool = ConnectionPool(conninfo=DATABASE_URL)
except Exception as e:
    print("Error connecting to database")
    print(e)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    # with pool.connection() as conn:
    #     with conn.cursor() as cursor:
    #         posts = cursor.execute("SELECT * FROM posts").fetchall()
    

    return db.scalars(select(Post)).all()
         

@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # with pool.connection() as conn:
    #     with conn.cursor() as cursor:
    #         cursor.execute(
    #             """SELECT * 
    #             FROM posts
    #             WHERE id = %s;""",
    #             (id,)
    #         )
    #         post = cursor.fetchone()
    #     if not post:
    #         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                         detail=f"Can't find a post with ID {id}")
    #     return {"post": post}


    #? Explicit way of writing the query
    # stmt = select(Post).where(Post.id == id)
    # post = db.execute(stmt).scalar_one_or_none()
    
    #? Getting post by primary key
    post = db.get(Post, id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Can't find a post with ID {id}")
    return post


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # with pool.connection() as conn:
    #     with conn.cursor() as cursor:
    #         cursor.execute(
    #             """INSERT INTO posts (title, content, published)
    #             VALUES (%s, %s, %s)
    #             RETURNING *;""", 
    #             (post.title, post.content, post.published)
    #         )
    #     conn.commit()
    #     return { "new_post": cursor.fetchone()}


    # new_post = Post(title=post.title, content=post.content, published=post.published)
    new_post = Post(**post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    # with pool.connection() as conn:
    #     with conn.cursor() as cursor:
    #         cursor.execute(
    #             """DELETE FROM posts
    #             WHERE id=%s
    #             RETURNING *;""",
    #             (id,)
    #         )
    #         post_to_delete = cursor.fetchone()
    #         if not post_to_delete:
    #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                                 detail=f"Post with ID '{id}' not found")

    #         return

    
        
    #? ORM-Style deletion

    #? Explicit way of writing the query
    # stmt = select(Post).where(Post.id == id)
    # post_to_delete = db.execute(stmt).scalar_one_or_none()
    
    #? Getting post by primary key
    post_to_delete = db.get(Post, id)
    if not post_to_delete:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Can't find a post with ID {id}")
    db.delete(post_to_delete)

    #? More efficient, but without ORM Events triggered. Pretty sure, this way is used for SQLAlchemy 1.x
    # post_query = db.query(Post).filter(Post.id == id)
    # if not post_query.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f"Can't find a post with ID {id}")
    # post_query.delete(synchronize_session=False)
    
    db.commit()
    return

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def update_post(id: int, post: PostBase, db: Session = Depends(get_db)):
    # with pool.connection() as conn:
    #     with conn.cursor() as cursor:
    #         cursor.execute(
    #             """UPDATE posts
    #             SET title=%s, content=%s, published=%s
    #             WHERE id=%s
    #             RETURNING *;""",
    #             (post.title, post.content, post.published, id)
    #         )
    #         updated_post = cursor.fetchone()
    #         if not updated_post:
    #             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                                 detail=f"Post with ID '{id}' not found")
    #         conn.commit()
            
    #         return {"data" : updated_post}
    
    

    #? Non-ORM Update

    #? Explicit way of writing the query
    stmt = (update(Post)
            .where(Post.id == id)
            .values(**post.model_dump())
            .returning(Post)
            )
            
    post_to_update = db.execute(stmt)

    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Can't find a post with ID {id}")
    
    db.commit()
    # Don't know why, but putting .scalar_one_or_none() before commit() doesn't work
    return post_to_update.scalar_one_or_none()