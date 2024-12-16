
from fastapi import APIRouter
from typing import List
from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from sqlalchemy import select, text, update
from sqlalchemy.orm import Session
from ..db.models import Post
from ..db.database import get_db
from ..schemas.schemas import PostCreate, PostResponse, PostUpdate


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/", response_model=List[PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.scalars(select(Post)).all()
         

@router.get("/{id}", response_model=PostResponse)
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


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    # new_post = Post(title=post.title, content=post.content, published=post.published)
    new_post = Post(**post.model_dump())
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post
    

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
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

@router.put("/{id}", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
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
