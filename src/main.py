from typing import List
from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from sqlalchemy import select, text, update
from sqlalchemy.orm import Session
from .db.models import Post, Base, User
from .db.database import engine, get_db
from .routers import posts, users, auth

#! User Alembic in production instead of create_all()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="My FastAPI Application",
    version="0.0.1",)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
async def root():
    return {"message": "Welcome to my API"}
