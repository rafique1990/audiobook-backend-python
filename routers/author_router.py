from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session, select
from typing import List

from schema import Author, AuthorCreate, AuthorRead
from database import get_session

router = APIRouter()


@router.post("/", response_model=AuthorRead)
def create_author(author: AuthorCreate, session: Session = Depends(get_session)):
    db_author = Author.from_orm(author)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@router.get("/{author_id}", response_model=AuthorRead)
def read_author(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    return author


@router.get("/", response_model=List[AuthorRead])
def list_authors(
    skip: int = 0, limit: int = 10, session: Session = Depends(get_session)
):
    authors = session.exec(select(Author).offset(skip).limit(limit)).all()
    return authors


@router.put("/{author_id}", response_model=AuthorRead)
def update_author(
    author_id: int, author: AuthorCreate, session: Session = Depends(get_session)
):
    db_author = session.get(Author, author_id)
    if not db_author:
        raise HTTPException(status_code=404, detail="Author not found")
    author_data = author.dict(exclude_unset=True)
    for key, value in author_data.items():
        setattr(db_author, key, value)
    session.add(db_author)
    session.commit()
    session.refresh(db_author)
    return db_author


@router.delete("/{author_id}")
def delete_author(author_id: int, session: Session = Depends(get_session)):
    author = session.get(Author, author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Author not found")
    session.delete(author)
    session.commit()
    return {"ok": True}
