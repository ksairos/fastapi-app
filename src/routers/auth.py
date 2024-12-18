from datetime import timedelta

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.auth.oauth2 import create_access_token
from src.db.database import get_db
from src.db.models import User
from src.schemas.schemas import UserLogin
from src.auth.hashing import verify

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/")
def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    stmt = (
        select(User)
        .where(User.email == user_credentials.email))
    user = db.execute(stmt).scalar_one_or_none()

    # Verify email
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect Email or Password. Try again!"
        )

    # Verify password
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Incorrect Email or Password. Try again!"
        )

    access_token = create_access_token(
        data={
            "user_id" : user.id,
        },
    )

    return {"access_token" : access_token, "token_type" : "bearer"}