from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase

class Base(DeclarativeBase):
    pass

SQLALCHEMY_DATABASE_URL = URL.create(
    drivername="postgresql+psycopg",
    username="postgres",
    password="1298",
    host="localhost",
    database="fastapi",
    port=5432)

engine = create_engine(SQLALCHEMY_DATABASE_URL)
session_local = sessionmaker(autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()