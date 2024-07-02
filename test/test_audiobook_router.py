import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import Audiobook, Author, Narrator
from datetime import datetime

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
async def test_create_audiobook(async_client, session):
    author = Author(name="Author One", bio="Bio of Author One")
    narrator = Narrator(name="Narrator One", bio="Bio of Narrator One")
    session.add(author)
    session.add(narrator)
    session.commit()
    session.refresh(author)
    session.refresh(narrator)

    response = await async_client.post("/audiobooks/", json={
        "title": "Audiobook One",
        "author_id": author.author_id,
        "narrator_id": narrator.narrator_id,
        "duration": 3600,
        "description": "Description for audiobook one",
        "release_date": datetime(2023, 1, 1, 0, 0, 0).isoformat()
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Audiobook One"

@pytest.mark.asyncio
async def test_read_audiobook(async_client, session):
    author = Author(name="Author One", bio="Bio of Author One")
    narrator = Narrator(name="Narrator One", bio="Bio of Narrator One")
    audiobook = Audiobook(
        title="Audiobook One",
        author_id=author.author_id,
        narrator_id=narrator.narrator_id,
        duration=3600,
        description="Description for audiobook one",
        release_date=datetime(2023, 1, 1, 0, 0, 0)
    )
    session.add(author)
    session.add(narrator)
    session.add(audiobook)
    session.commit()
    session.refresh(audiobook)

    response = await async_client.get(f"/audiobooks/{audiobook.audiobook_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Audiobook One"

@pytest.mark.asyncio
async def test_list_audiobooks(async_client, session):
    author = Author(name="Author One", bio="Bio of Author One")
    narrator = Narrator(name="Narrator One", bio="Bio of Narrator One")
    audiobook1 = Audiobook(
        title="Audiobook One",
        author_id=author.author_id,
        narrator_id=narrator.narrator_id,
        duration=3600,
        description="Description for audiobook one",
        release_date=datetime(2023, 1, 1, 0, 0, 0)
    )
    audiobook2 = Audiobook(
        title="Audiobook Two",
        author_id=author.author_id,
        narrator_id=narrator.narrator_id,
        duration=4200,
        description="Description for audiobook two",
        release_date=datetime(2023, 2, 1, 0, 0, 0)
    )
    session.add(author)
    session.add(narrator)
    session.add(audiobook1)
    session.add(audiobook2)
    session.commit()

    response = await async_client.get("/audiobooks/")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_update_audiobook(async_client, session):
    author = Author(name="Author One", bio="Bio of Author One")
    narrator = Narrator(name="Narrator One", bio="Bio of Narrator One")
    audiobook = Audiobook(
        title="Audiobook One",
        author_id=author.author_id,
        narrator_id=narrator.narrator_id,
        duration=3600,
        description="Description for audiobook one",
        release_date=datetime(2023, 1, 1, 0, 0, 0)
    )
    session.add(author)
    session.add(narrator)
    session.add(audiobook)
    session.commit()
    session.refresh(audiobook)

    response = await async_client.put(f"/audiobooks/{audiobook.audiobook_id}", json={
        "title": "Updated Audiobook One",
        "author_id": author.author_id,
        "narrator_id": narrator.narrator_id,
        "duration": 3600,
        "description": "Updated description for audiobook one",
        "release_date": datetime(2023, 1, 1, 0, 0, 0).isoformat()
    })
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Audiobook One"

@pytest.mark.asyncio
async def test_delete_audiobook(async_client, session):
    author = Author(name="Author One", bio="Bio of Author One")
    narrator = Narrator(name="Narrator One", bio="Bio of Narrator One")
    audiobook = Audiobook(
        title="Audiobook One",
        author_id=author.author_id,
        narrator_id=narrator.narrator_id,
        duration=3600,
        description="Description for audiobook one",
        release_date=datetime(2023, 1, 1, 0, 0, 0)
    )
    session.add(author)
    session.add(narrator)
    session.add(audiobook)
    session.commit()
    session.refresh(audiobook)

    response = await async_client.delete(f"/audiobooks/{audiobook.audiobook_id}")
    assert response.status_code == 200
    assert response.json()["title"] == "Audiobook One"
