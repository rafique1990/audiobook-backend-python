from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from schema import Bookmark, BookmarkCreate, BookmarkRead
from database import get_session

router = APIRouter()


@router.post("/", response_model=BookmarkRead)
def create_bookmark(bookmark: BookmarkCreate, session: Session = Depends(get_session)):
    db_bookmark = Bookmark.from_orm(bookmark)
    session.add(db_bookmark)
    session.commit()
    session.refresh(db_bookmark)
    return db_bookmark


@router.get("/{bookmark_id}", response_model=BookmarkRead)
def read_bookmark(bookmark_id: int, session: Session = Depends(get_session)):
    bookmark = session.get(Bookmark, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return bookmark


@router.get("/", response_model=List[BookmarkRead])
def list_bookmarks(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    bookmarks = session.exec(select(Bookmark).offset(skip).limit(limit)).all()
    return bookmarks


@router.put("/{bookmark_id}", response_model=BookmarkRead)
def update_bookmark(
    bookmark_id: int, bookmark: BookmarkCreate, session: Session = Depends(get_session)
):
    db_bookmark = session.get(Bookmark, bookmark_id)
    if not db_bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    bookmark_data = bookmark.dict(exclude_unset=True)
    for key, value in bookmark_data.items():
        setattr(db_bookmark, key, value)
    session.add(db_bookmark)
    session.commit()
    session.refresh(db_bookmark)
    return db_bookmark


@router.delete("/{bookmark_id}")
def delete_bookmark(bookmark_id: int, session: Session = Depends(get_session)):
    bookmark = session.get(Bookmark, bookmark_id)
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    session.delete(bookmark)
    session.commit()
    return {"ok": True}
