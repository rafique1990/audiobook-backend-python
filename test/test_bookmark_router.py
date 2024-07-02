import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import Bookmark, User, Audiobook, Chapter

DATABASE_URL = "sqlite:///test_audiobook_app.db"
engine = create_engine(DATABASE_URL, echo=True)

@pytest.fixture
def session():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_create_bookmark(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    chapter = Chapter(audiobook_id=1, title="Chapter One", duration=600, position=1)
    session.add(user)
    session.add(audiobook)
    session.add(chapter)
    session.commit()
    session.refresh(user)
    session.refresh(audiobook)
    session.refresh(chapter)

    response = await async_client.post("/bookmarks/", json={
        "user_id": user.user_id,
        "audiobook_id": audiobook.audiobook_id,
        "chapter_id": chapter.chapter_id,
        "position": 300
    })
    assert response.status_code == 200
    assert response.json()["position"] == 300

@pytest.mark.asyncio
async def test_read_bookmark(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    chapter = Chapter(audiobook_id=1, title="Chapter One", duration=600, position=1)
    bookmark = Bookmark(user_id=1, audiobook_id=1, chapter_id=1, position=300)
    session.add(user)
    session.add(audiobook)
    session.add(chapter)
    session.add(bookmark)
    session.commit()
    session.refresh(bookmark)

    response = await async_client.get(f"/bookmarks/{bookmark.bookmark_id}")
    assert response.status_code == 200
    assert response.json()["position"] == 300

@pytest.mark.asyncio
async def test_list_bookmarks(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    chapter = Chapter(audiobook_id=1, title="Chapter One", duration=600, position=1)
    bookmark1 = Bookmark(user_id=1, audiobook_id=1, chapter_id=1, position=300)
    bookmark2 = Bookmark(user_id=1, audiobook_id=1, chapter_id=1, position=600)
    session.add(user)
    session.add(audiobook)
    session.add(chapter)
    session.add(bookmark1)
    session.add(bookmark2)
    session.commit()

    response = await async_client.get("/bookmarks/")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_update_bookmark(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    chapter = Chapter(audiobook_id=1, title="Chapter One", duration=600, position=1)
    bookmark = Bookmark(user_id=1, audiobook_id=1, chapter_id=1, position=300)
    session.add(user)
    session.add(audiobook)
    session.add(chapter)
    session.add(bookmark)
    session.commit()
    session.refresh(bookmark)

    response = await async_client.put(f"/bookmarks/{bookmark.bookmark_id}", json={
        "user_id": user.user_id,
        "audiobook_id": audiobook.audiobook_id,
        "chapter_id": chapter.chapter_id,
        "position": 600
    })
    assert response.status_code == 200
    assert response.json()["position"] == 600

@pytest.mark.asyncio
async def test_delete_bookmark(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    chapter = Chapter(audiobook_id=1, title="Chapter One", duration=600, position=1)
    bookmark = Bookmark(user_id=1, audiobook_id=1, chapter_id=1, position=300)
    session.add(user)
    session.add(audiobook)
    session.add(chapter)
    session.add(bookmark)
    session.commit()
    session.refresh(bookmark)

    response = await async_client.delete(f"/bookmarks/{bookmark.bookmark_id}")
    assert response.status_code == 200
    assert response.json()["position"] == 300
