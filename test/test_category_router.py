import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import Category

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
async def test_create_category(async_client):
    response = await async_client.post("/categories/", json={
        "name": "Fiction"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Fiction"

@pytest.mark.asyncio
async def test_read_category(async_client, session):
    category = Category(name="Fiction")
    session.add(category)
    session.commit()
    session.refresh(category)

    response = await async_client.get(f"/categories/{category.category_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Fiction"

@pytest.mark.asyncio
async def test_list_categories(async_client, session):
    category1 = Category(name="Fiction")
    category2 = Category(name="Non-Fiction")
    session.add(category1)
    session.add(category2)
    session.commit()

    response = await async_client.get("/categories/")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_update_category(async_client, session):
    category = Category(name="Fiction")
    session.add(category)
    session.commit()
    session.refresh(category)

    response = await async_client.put(f"/categories/{category.category_id}", json={
        "name": "Updated Fiction"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Fiction"

@pytest.mark.asyncio
async def test_delete_category(async_client, session):
    category = Category(name="Fiction")
    session.add(category)
    session.commit()
    session.refresh(category)

    response = await async_client.delete(f"/categories/{category.category_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Fiction"
