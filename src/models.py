from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, text
from .database import Base

class Post(Base):
    # To modify the table use Alembic for database migrations
    # Anything changed here doesn't affect existing database
    # If anything changed here, delete the table and rerun the code
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, nullable=False, server_default='TRUE')
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    