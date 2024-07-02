import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import Subscription

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
async def test_create_subscription(async_client):
    response = await async_client.post("/subscriptions/", json={
        "name": "Premium",
        "price": 9.99,
        "duration_days": 30
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Premium"

@pytest.mark.asyncio
async def test_read_subscription(async_client, session):
    subscription = Subscription(name="Premium", price=9.99, duration_days=30)
    session.add(subscription)
    session.commit()
    session.refresh(subscription)

    response = await async_client.get(f"/subscriptions/{subscription.subscription_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Premium"

@pytest.mark.asyncio
async def test_list_subscriptions(async_client, session):
    subscription1 = Subscription(name="Premium", price=9.99, duration_days=30)
    subscription2 = Subscription(name="Basic", price=4.99, duration_days=30)
    session.add(subscription1)
    session.add(subscription2)
    session.commit()

    response = await async_client.get("/subscriptions/")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_update_subscription(async_client, session):
    subscription = Subscription(name="Premium", price=9.99, duration_days=30)
    session.add(subscription)
    session.commit()
    session.refresh(subscription)

    response = await async_client.put(f"/subscriptions/{subscription.subscription_id}", json={
        "name": "Updated Premium",
        "price": 14.99,
        "duration_days": 60
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Premium"

@pytest.mark.asyncio
async def test_delete_subscription(async_client, session):
    subscription = Subscription(name="Premium", price=9.99, duration_days=30)
    session.add(subscription)
    session.commit()
    session.refresh(subscription)

    response = await async_client.delete(f"/subscriptions/{subscription.subscription_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Premium"