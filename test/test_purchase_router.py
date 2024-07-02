import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import Purchase, User, Audiobook
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
async def test_create_purchase(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    session.add(user)
    session.add(audiobook)
    session.commit()
    session.refresh(user)
    session.refresh(audiobook)

    response = await async_client.post("/purchases/", json={
        "user_id": user.user_id,
        "audiobook_id": audiobook.audiobook_id,
        "purchase_date": datetime(2023, 1, 1, 0, 0, 0).isoformat()
    })
    assert response.status_code == 200
    assert response.json()["user_id"] == user.user_id

@pytest.mark.asyncio
async def test_read_purchase(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    purchase = Purchase(
        user_id=user.user_id,
        audiobook_id=audiobook.audiobook_id,
        purchase_date=datetime(2023, 1, 1, 0, 0, 0)
    )
    session.add(user)
    session.add(audiobook)
    session.add(purchase)
    session.commit()
    session.refresh(purchase)

    response = await async_client.get(f"/purchases/{purchase.purchase_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user.user_id

@pytest.mark.asyncio
async def test_list_purchases(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    purchase1 = Purchase(
        user_id=user.user_id,
        audiobook_id=audiobook.audiobook_id,
        purchase_date=datetime(2023, 1, 1, 0, 0, 0)
    )
    purchase2 = Purchase(
        user_id=user.user_id,
        audiobook_id=audiobook.audiobook_id,
        purchase_date=datetime(2023, 2, 1, 0, 0, 0)
    )
    session.add(user)
    session.add(audiobook)
    session.add(purchase1)
    session.add(purchase2)
    session.commit()

    response = await async_client.get("/purchases/")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_update_purchase(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    purchase = Purchase(
        user_id=user.user_id,
        audiobook_id=audiobook.audiobook_id,
        purchase_date=datetime(2023, 1, 1, 0, 0, 0)
    )
    session.add(user)
    session.add(audiobook)
    session.add(purchase)
    session.commit()
    session.refresh(purchase)

    response = await async_client.put(f"/purchases/{purchase.purchase_id}", json={
        "user_id": user.user_id,
        "audiobook_id": audiobook.audiobook_id,
        "purchase_date": datetime(2023, 1, 2, 0, 0, 0).isoformat()
    })
    assert response.status_code == 200
    assert response.json()["purchase_date"] == "2023-01-02T00:00:00"

@pytest.mark.asyncio
async def test_delete_purchase(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    audiobook = Audiobook(title="Audiobook One", author_id=1, narrator_id=1, duration=3600)
    purchase = Purchase(
        user_id=user.user_id,
        audiobook_id=audiobook.audiobook_id,
        purchase_date=datetime(2023, 1, 1, 0, 0, 0)
    )
    session.add(user)
    session.add(audiobook)
    session.add(purchase)
    session.commit()
    session.refresh(purchase)

    response = await async_client.delete(f"/purchases/{purchase.purchase_id}")
    assert response.status_code == 200
    assert response.json()["user_id"] == user.user_id
