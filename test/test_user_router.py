import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import User

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
async def test_create_user(async_client):
    response = await async_client.post("/users/", json={
        "username": "user1",
        "name": "John Doe",
        "email": "john@example.com",
        "password": "secretpassword"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "user1"

@pytest.mark.asyncio
async def test_read_user(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    session.add(user)
    session.commit()
    session.refresh(user)

    response = await async_client.get(f"/users/{user.user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "user1"

@pytest.mark.asyncio
async def test_list_users(async_client, session):
    user1 = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    user2 = User(username="user2", name="Jane Doe", email="jane@example.com", password="secretpassword")
    session.add(user1)
    session.add(user2)
    session.commit()

    response = await async_client.get("/users/")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_update_user(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    session.add(user)
    session.commit()
    session.refresh(user)

    response = await async_client.put(f"/users/{user.user_id}", json={
        "username": "updateduser",
        "name": "John Updated",
        "email": "john.updated@example.com",
        "password": "newsecretpassword"
    })
    assert response.status_code == 200
    assert response.json()["username"] == "updateduser"

@pytest.mark.asyncio
async def test_delete_user(async_client, session):
    user = User(username="user1", name="John Doe", email="john@example.com", password="secretpassword")
    session.add(user)
    session.commit()
    session.refresh(user)

    response = await async_client.delete(f"/users/{user.user_id}")
    assert response.status_code == 200
    assert response.json()["username"] == "user1"
