from typing import List
from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from sqlalchemy import select, text, update
from sqlalchemy.orm import Session
from .models import Post, Base, User
from .database import engine, get_db
from .schemas import PostCreate, PostResponse, PostUpdate, UserCreate, UserResponse


#! User Alembic in production instead of create_all()
Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}


@app.get("/posts", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.scalars(select(Post)).all()
         

@app.get("/posts/{id}", response_model=PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):

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
    # new_post = Post(title=post.title, content=post.content, published=post.published)
    new_post = Post(**post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    
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
    # post_to_delete = db.get(Post, id)
    # if not post_query.first():
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
    #                     detail=f"Can't find a post with ID {id}")
    # post_query.delete(synchronize_session=False)
    
    db.commit()
    return

@app.put("/posts/{id}", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def update_post(id: int, post: PostUpdate, db: Session = Depends(get_db)):

    #? Non-ORM Update

    #? Explicit way of writing the query
    stmt = (update(Post)
            .where(Post.id == id)
            .values(**post.model_dump())
            .returning(Post)
            )
            
    post_to_update = db.execute(stmt).scalar_one_or_none()
    if not post_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Can't find a post with ID {id}")
    
    db.commit()
    return post_to_update


@app.get("/users", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.scalars(select(User)).all()


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(**user.model_dump())  

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@app.get("/users/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with id {id} doesn't exist")
    return user