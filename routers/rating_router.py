from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from schema import Rating, RatingCreate, RatingRead
from database import get_session

router = APIRouter()


@router.post("/", response_model=RatingRead)
def create_rating(rating: RatingCreate, session: Session = Depends(get_session)):
    db_rating = Rating.from_orm(rating)
    session.add(db_rating)
    session.commit()
    session.refresh(db_rating)
    return db_rating


@router.get("/{rating_id}", response_model=RatingRead)
def read_rating(rating_id: int, session: Session = Depends(get_session)):
    rating = session.get(Rating, rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return rating


@router.get("/", response_model=List[RatingRead])
def list_ratings(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    ratings = session.exec(select(Rating).offset(skip).limit(limit)).all()
    return ratings


@router.put("/{rating_id}", response_model=RatingRead)
def update_rating(
    rating_id: int, rating: RatingCreate, session: Session = Depends(get_session)
):
    db_rating = session.get(Rating, rating_id)
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    rating_data = rating.dict(exclude_unset=True)
    for key, value in rating_data.items():
        setattr(db_rating, key, value)
    session.add(db_rating)
    session.commit()
    session.refresh(db_rating)
    return db_rating


@router.delete("/{rating_id}")
def delete_rating(rating_id: int, session: Session = Depends(get_session)):
    rating = session.get(Rating, rating_id)
    if not rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    session.delete(rating)
    session.commit()
    return {"ok": True}
