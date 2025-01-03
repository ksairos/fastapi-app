from fastapi import APIRouter, status, Depends, HTTPException
from sqlalchemy.event import remove
from sqlalchemy.orm import Session
from sqlalchemy import select

from src.auth.oauth2 import get_current_user
from src.db.database import get_db
from src.db.models import UserModel, VoteModel, PostModel
from src.schemas.schemas import Vote

router = APIRouter(
    # Instead of writing "/users" in each endpoint
    prefix="/vote",
    # Grouping endpoints for documentation
    tags=["Vote"]
)

@router.get("/")
def get_votes(db: Session = Depends(get_db)):
    stmt = select(VoteModel)
    return db.scalars(stmt).all()


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
        vote: Vote,
        db: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_user)
):
    # Check if post exists
    post = db.get(PostModel, vote.post_id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Can't find a post with ID {vote.post_id}")

    # stmt = select(VoteModel).where(VoteModel.post_id == vote.post_id, VoteModel.user_id == current_user.id)
    existing_vote = db.get(VoteModel, (vote.post_id, current_user.id))

    # Remove like
    if existing_vote:
        db.delete(existing_vote)
        db.commit()
        return

    # Like the post
    new_vote = VoteModel(user_id=current_user.id, post_id=vote.post_id)
    db.add(new_vote)
    db.commit()
    db.refresh(new_vote)

    return new_vote

