import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import Chapter, Audiobook

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
async def test_create_chapter(async_client, session):
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    session.add(audiobook)
    session.commit()
    session.refresh(audiobook)

    response = await async_client.post("/chapters/", json={
        "audiobook_id": audiobook.audiobook_id,
        "title": "Chapter One",
        "duration": 600,
        "position": 1
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Chapter One"

@pytest.mark.asyncio
async def test_read_chapter(async_client, session):
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    chapter = Chapter(audiobook_id=1, title="Chapter One", duration=600, position=1)
    session.add(audiobook)
    session.add(chapter)
    session.commit()
    session.refresh(chapter)

    response = await async_client.get(f"/chapters/{chapter.chapter_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Chapter One"

@pytest.mark.asyncio
async def test_list_chapters(async_client, session):
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    chapter1 = Chapter(audiobook_id=1, title="Chapter One", duration=600, position=1)
    chapter2 = Chapter(audiobook_id=1, title="Chapter Two", duration=700, position=2)
    session.add(audiobook)
    session.add(chapter1)
    session.add(chapter2)
    session.commit()

    response = await async_client.get("/chapters/")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_update_chapter(async_client, session):
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    chapter = Chapter(audiobook_id=1, title="Chapter One", duration=600, position=1)
    session.add(audiobook)
    session.add(chapter)
    session.commit()
    session.refresh(chapter)

    response = await async_client.put(f"/chapters/{chapter.chapter_id}", json={
        "audiobook_id": audiobook.audiobook_id,
        "title": "Updated Chapter One",
        "duration": 600,
        "position": 1
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Chapter One"

@pytest.mark.asyncio
async def test_delete_chapter(async_client, session):
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    chapter = Chapter(audiobook_id=1, title="Chapter One", duration=600, position=1)
    session.add(audiobook)
    session.add(chapter)
    session.commit()
    session.refresh(chapter)

    response = await async_client.delete(f"/chapters/{chapter.chapter_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Chapter One"
