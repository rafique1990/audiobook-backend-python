from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from schema import ListeningHistory, ListeningHistoryCreate, ListeningHistoryRead
from database import get_session

router = APIRouter()


@router.post("/", response_model=ListeningHistoryRead)
def create_listening_history(
    listening_history: ListeningHistoryCreate, session: Session = Depends(get_session)
):
    db_listening_history = ListeningHistory.from_orm(listening_history)
    session.add(db_listening_history)
    session.commit()
    session.refresh(db_listening_history)
    return db_listening_history


@router.get("/{listening_history_id}", response_model=ListeningHistoryRead)
def read_listening_history(
    listening_history_id: int, session: Session = Depends(get_session)
):
    listening_history = session.get(ListeningHistory, listening_history_id)
    if not listening_history:
        raise HTTPException(status_code=404, detail="ListeningHistory not found")
    return listening_history


@router.get("/", response_model=List[ListeningHistoryRead])
def list_listening_histories(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    listening_histories = session.exec(
        select(ListeningHistory).offset(skip).limit(limit)
    ).all()
    return listening_histories


@router.put("/{listening_history_id}", response_model=ListeningHistoryRead)
def update_listening_history(
    listening_history_id: int,
    listening_history: ListeningHistoryCreate,
    session: Session = Depends(get_session),
):
    db_listening_history = session.get(ListeningHistory, listening_history_id)
    if not db_listening_history:
        raise HTTPException(status_code=404, detail="ListeningHistory not found")
    listening_history_data = listening_history.dict(exclude_unset=True)
    for key, value in listening_history_data.items():
        setattr(db_listening_history, key, value)
    session.add(db_listening_history)
    session.commit()
    session.refresh(db_listening_history)
    return db_listening_history


@router.delete("/{listening_history_id}")
def delete_listening_history(
    listening_history_id: int, session: Session = Depends(get_session)
):
    listening_history = session.get(ListeningHistory, listening_history_id)
    if not listening_history:
        raise HTTPException(status_code=404, detail="ListeningHistory not found")
    session.delete(listening_history)
    session.commit()
    return {"ok": True}
