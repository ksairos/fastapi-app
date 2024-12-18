from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.auth.oauth2 import create_access_token
from src.db.database import get_db
from src.db.models import User
from src.auth.hashing import verify
from src.schemas.schemas import Token

router = APIRouter(
    prefix="/login",
    tags=["Authentication"]
)

@router.post("/", response_model=Token)
def login(user_credentials: Annotated[OAuth2PasswordRequestForm, Depends()], db: Session = Depends(get_db)):
    stmt = (
        select(User)
        .where(User.email == user_credentials.username))
    user = db.execute(stmt).scalar_one_or_none()

    # Verify email
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect Email or Password. Try again!"
        )

    # Verify password
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Incorrect Email or Password. Try again!"
        )

    access_token = create_access_token(
        data={
            "user_id" : user.id,
        },
    )

    return {"access_token" : access_token, "token_type" : "bearer"}