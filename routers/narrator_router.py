from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from schema import Narrator, NarratorCreate, NarratorRead
from database import get_session

router = APIRouter()


@router.post("/", response_model=NarratorRead)
def create_narrator(narrator: NarratorCreate, session: Session = Depends(get_session)):
    db_narrator = Narrator.from_orm(narrator)
    session.add(db_narrator)
    session.commit()
    session.refresh(db_narrator)
    return db_narrator


@router.get("/{narrator_id}", response_model=NarratorRead)
def read_narrator(narrator_id: int, session: Session = Depends(get_session)):
    narrator = session.get(Narrator, narrator_id)
    if not narrator:
        raise HTTPException(status_code=404, detail="Narrator not found")
    return narrator


@router.get("/", response_model=List[NarratorRead])
def list_narrators(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    narrators = session.exec(select(Narrator).offset(skip).limit(limit)).all()
    return narrators


@router.put("/{narrator_id}", response_model=NarratorRead)
def update_narrator(
    narrator_id: int, narrator: NarratorCreate, session: Session = Depends(get_session)
):
    db_narrator = session.get(Narrator, narrator_id)
    if not db_narrator:
        raise HTTPException(status_code=404, detail="Narrator not found")
    narrator_data = narrator.dict(exclude_unset=True)
    for key, value in narrator_data.items():
        setattr(db_narrator, key, value)
    session.add(db_narrator)
    session.commit()
    session.refresh(db_narrator)
    return db_narrator
