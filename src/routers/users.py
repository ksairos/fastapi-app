from fastapi import APIRouter
from typing import List
from fastapi import status, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..auth.hashing import hash_fn
from ..db.models import User
from ..db.database import get_db
from ..schemas.schemas import UserCreate, UserResponse
from ..auth import hashing

router = APIRouter(
    # Instead of writing "/users" in each endpoint
    prefix="/users",
    # Grouping endpoints for documentation
    tags=["Users"]
)

@router.get("/", response_model=List[UserResponse])
def get_users(db: Session = Depends(get_db)):
    return db.scalars(select(User)).all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    # Hash the user password
    user.password = hash_fn(user.password)

    new_user = User(**user.model_dump())  
    
    db.add(new_user)

    # TODO add duplicate email handling
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}", response_model=UserResponse)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.get(User, id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"User with id {id} doesn't exist")
    return user