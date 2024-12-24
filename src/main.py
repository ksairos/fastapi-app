from fastapi import FastAPI
from fastapi import FastAPI

from .db.database import engine
from .db.models import Base
from .routers import posts, users, auth

# ! User Alembic in production instead of create_all()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My FastAPI Application",
    version="0.0.1", )

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}
