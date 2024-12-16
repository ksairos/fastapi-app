from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Hash the user password
def hash(password: str):
    return pwd_context.hash(password)
