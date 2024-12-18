from datetime import timedelta, datetime, timezone
import jwt
from fastapi import HTTPException, status
from fastapi.params import Depends
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session
from sqlalchemy import select
from src.db.database import get_db
from src.db.models import User
from src.schemas.schemas import TokenData
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = "3f8cbe0d238600f8961208ba0de2593e75fc10b9138c15a48d6fbe6e12553c72"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


# Creates a JWT Token, that's it
def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Decode the token and return the payload (main body of the token)
def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = payload.get("user_id")

        if not id:
            raise credential_exception
        token_data = TokenData(id=user_id)
    except InvalidTokenError:
        raise credential_exception

    return token_data


# This function is used for a dependency injection in path functions
# If the token is invalid or expired, credentials_exception is called
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token_data = verify_access_token(token, credentials_exception)
    user = db.get(User, token_data.id)

    return user
