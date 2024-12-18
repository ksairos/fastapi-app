from datetime import timedelta, datetime, timezone

import jwt
from jwt.exceptions import InvalidTokenError

SECRET_KEY = "3f8cbe0d238600f8961208ba0de2593e75fc10b9138c15a48d6fbe6e12553c72"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict) -> str:
    to_encode = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp" : expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt