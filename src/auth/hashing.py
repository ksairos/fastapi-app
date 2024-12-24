from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash the user password
def hash_fn(password: str) -> str:
    return pwd_context.hash(password)


# Verify that the input password is the same with hashed from DB
def verify(raw_password, hashed_password) -> bool:
    return pwd_context.verify(raw_password, hashed_password)