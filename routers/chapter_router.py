from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from schema import Chapter, ChapterCreate, ChapterRead
from database import get_session

router = APIRouter()


@router.post("/", response_model=ChapterRead)
def create_chapter(chapter: ChapterCreate, session: Session = Depends(get_session)):
    db_chapter = Chapter.from_orm(chapter)
    session.add(db_chapter)
    session.commit()
    session.refresh(db_chapter)
    return db_chapter


@router.get("/{chapter_id}", response_model=ChapterRead)
def read_chapter(chapter_id: int, session: Session = Depends(get_session)):
    chapter = session.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    return chapter


@router.get("/", response_model=List[ChapterRead])
def list_chapters(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    chapters = session.exec(select(Chapter).offset(skip).limit(limit)).all()
    return chapters


@router.put("/{chapter_id}", response_model=ChapterRead)
def update_chapter(
    chapter_id: int, chapter: ChapterCreate, session: Session = Depends(get_session)
):
    db_chapter = session.get(Chapter, chapter_id)
    if not db_chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    chapter_data = chapter.dict(exclude_unset=True)
    for key, value in chapter_data.items():
        setattr(db_chapter, key, value)
    session.add(db_chapter)
    session.commit()
    session.refresh(db_chapter)
    return db_chapter


@router.delete("/{chapter_id}")
def delete_chapter(chapter_id: int, session: Session = Depends(get_session)):
    chapter = session.get(Chapter, chapter_id)
    if not chapter:
        raise HTTPException(status_code=404, detail="Chapter not found")
    session.delete(chapter)
    session.commit()
    return {"ok": True}
