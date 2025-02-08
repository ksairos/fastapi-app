import logging

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker, DeclarativeBase

from src.config import settings


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class Base(DeclarativeBase):
    pass

SQLALCHEMY_DATABASE_URI = URL.create(
    drivername="postgresql+psycopg",
    username=settings.database_username,
    password=settings.database_password,
    host=settings.database_host,
    database=settings.database_name,
    port=settings.database_port)

print()
print("SQLALCHEMY_DATABASE_URI: ", SQLALCHEMY_DATABASE_URI.render_as_string(hide_password=False))
print()

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session_local = sessionmaker(autoflush=False, bind=engine)

# Dependency to get the database session
def get_db():
    database = session_local()
    try:
        yield database
    finally:
        database.close()