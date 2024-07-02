from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from schema import Audiobook, AudiobookCreate, AudiobookRead
from database import get_session


router = APIRouter()


@router.post("/", response_model=AudiobookRead)
def create_audiobook(
    audiobook: AudiobookCreate, session: Session = Depends(get_session)
):
    db_audiobook = Audiobook.from_orm(audiobook)
    session.add(db_audiobook)
    session.commit()
    session.refresh(db_audiobook)
    return db_audiobook


@router.get("/{audiobook_id}", response_model=AudiobookRead)
def read_audiobook(audiobook_id: int, session: Session = Depends(get_session)):
    audiobook = session.get(Audiobook, audiobook_id)
    if not audiobook:
        raise HTTPException(status_code=404, detail="Audiobook not found")
    return audiobook


@router.get("/", response_model=List[AudiobookRead])
def list_audiobooks(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    audiobooks = session.exec(select(Audiobook).offset(skip).limit(limit)).all()
    return audiobooks


@router.put("/{audiobook_id}", response_model=AudiobookRead)
def update_audiobook(
    audiobook_id: int,
    audiobook: AudiobookCreate,
    session: Session = Depends(get_session),
):
    db_audiobook = session.get(Audiobook, audiobook_id)
    if not db_audiobook:
        raise HTTPException(status_code=404, detail="Audiobook not found")
    audiobook_data = audiobook.dict(exclude_unset=True)
    for key, value in audiobook_data.items():
        setattr(db_audiobook, key, value)
    session.add(db_audiobook)
    session.commit()
    session.refresh(db_audiobook)
    return db_audiobook


@router.delete("/{audiobook_id}")
def delete_audiobook(audiobook_id: int, session: Session = Depends(get_session)):
    audiobook = session.get(Audiobook, audiobook_id)
    if not audiobook:
        raise HTTPException(status_code=404, detail="Audiobook not found")
    session.delete(audiobook)
    session.commit()
    return {"ok": True}
