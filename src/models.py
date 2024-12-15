from datetime import datetime
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
from sqlalchemy.orm import Mapped, mapped_column
from .database import Base

class Post(Base):
    # To modify the table use Alembic for database migrations
    # Anything changed here doesn't affect existing database
    # If anything changed here, delete the table and rerun the code
    __tablename__ = "posts"

    # id = Column(Integer, primary_key=True, nullable=False)
    # title = Column(String, nullable=False)
    # content = Column(String, nullable=False)
    # published = Column(Boolean, nullable=False, server_default='TRUE')
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    content: Mapped[str]
    published: Mapped[bool] = mapped_column(server_default="TRUE")
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))

class User(Base):
    __tablename__ = "users"
    
    # id = Column(Integer, primary_key=True, nullable=False)
    # email = Column(String, nullable=False, unique=True)
    # password = Column(String, nullable=False)
    # created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), server_default=text("now()"))