import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import ListeningHistory, User, Audiobook
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
async def test_create_listening_history(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    session.add(user)
    session.add(audiobook)
    session.commit()
    session.refresh(user)
    session.refresh(audiobook)

    response = await async_client.post("/listening_histories/", json={
        "user_id": user.user_id,
        "audiobook_id": audiobook.audiobook_id,
        "started_at": datetime(2023, 1, 1, 0, 0, 0).isoformat()
    })
    assert response.status_code == 200
    assert response.json()["user_id"] == user.user_id

@pytest.mark.asyncio
async def test_read_listening_history(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    listening_history = ListeningHistory(
        user_id=user.user_id,
        audiobook_id=audiobook.audiobook_id,
        started_at=datetime(2023, 1, 1, 0, 0, 0)
    )
    session.add(user)
    session.add(audiobook)
    session.add(listening_history)
    session.commit()
    session.refresh(listening_history)

    response = await async_client.get(f"/listening_histories/{listening_history.history_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user.user_id

@pytest.mark.asyncio
async def test_list_listening_histories(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    listening_history1 = ListeningHistory(
        user_id=user.user_id,
        audiobook_id=audiobook.audiobook_id,
        started_at=datetime(2023, 1, 1, 0, 0, 0)
    )
    listening_history2 = ListeningHistory(
        user_id=user.user_id,
        audiobook_id=audiobook.audiobook_id,
        started_at=datetime(2023, 2, 1, 0, 0, 0)
    )
    session.add(user)
    session.add(audiobook)
    session.add(listening_history1)
    session.add(listening_history2)
    session.commit()

    response = await async_client.get("/listening_histories/")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_update_listening_history(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    listening_history = ListeningHistory(
        user_id=user.user_id,
        audiobook_id=audiobook.audiobook_id,
        started_at=datetime(2023, 1, 1, 0, 0, 0)
    )
    session.add(user)
    session.add(audiobook)
    session.add(listening_history)
    session.commit()
    session.refresh(listening_history)

    response = await async_client.put(f"/listening_histories/{listening_history.history_id}", json={
        "user_id": user.user_id,
        "audiobook_id": audiobook.audiobook_id,
        "started_at": datetime(2023, 1, 1, 0, 0, 0).isoformat(),
        "finished_at": datetime(2023, 1, 2, 0, 0, 0).isoformat()
    })
    assert response.status_code == 200
    assert response.json()["finished_at"] == "2023-01-02T00:00:00"

@pytest.mark.asyncio
async def test_delete_listening_history(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    listening_history = ListeningHistory(
        user_id=user.user_id,
        audiobook_id=audiobook.audiobook_id,
        started_at=datetime(2023, 1, 1, 0, 0, 0)
    )
    session.add(user)
    session.add(audiobook)
    session.add(listening_history)
    session.commit()
    session.refresh(listening_history)

    response = await async_client.delete(f"/listening_histories/{listening_history.history_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user.user_id
