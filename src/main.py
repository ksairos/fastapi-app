from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db.database import engine
from .db.models import Base
from .routers import posts, users, auth, vote

## Use Alembic instead of create_all()
# Base.metadata.create_all(bind=engine)
app = FastAPI(
    title="My FastAPI Application",
    version="0.0.1", )

# Setting up CORS
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)


@app.get("/")
async def root():
    return {"message": "Welcome to my API"}
