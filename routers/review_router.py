from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from schema import Review, ReviewCreate, ReviewRead
from database import get_session

router = APIRouter()


@router.post("/", response_model=ReviewRead)
def create_review(review: ReviewCreate, session: Session = Depends(get_session)):
    db_review = Review.from_orm(review)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


@router.get("/{review_id}", response_model=ReviewRead)
def read_review(review_id: int, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    return review


@router.get("/", response_model=List[ReviewRead])
def list_reviews(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    reviews = session.exec(select(Review).offset(skip).limit(limit)).all()
    return reviews


@router.put("/{review_id}", response_model=ReviewRead)
def update_review(
    review_id: int, review: ReviewCreate, session: Session = Depends(get_session)
):
    db_review = session.get(Review, review_id)
    if not db_review:
        raise HTTPException(status_code=404, detail="Review not found")
    review_data = review.dict(exclude_unset=True)
    for key, value in review_data.items():
        setattr(db_review, key, value)
    session.add(db_review)
    session.commit()
    session.refresh(db_review)
    return db_review


@router.delete("/{review_id}")
def delete_review(review_id: int, session: Session = Depends(get_session)):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail="Review not found")
    session.delete(review)
    session.commit()
    return {"ok": True}
