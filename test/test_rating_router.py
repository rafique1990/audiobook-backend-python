import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import Rating, User, Audiobook

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
async def test_create_rating(async_client, session):
    user = User(
        username="user1", name="John Doe", email="john@example.com", password="password"
    )
    audiobook = Audiobook(
        title="Audiobook One",
        author_id=1,
        narrator_id=1,
        duration=3600,
        description="Description for audiobook one",
        release_date="2023-01-01T00:00:00",
    )
    session.add(user)
    session.add(audiobook)
    session.commit()
    session.refresh(user)
    session.refresh(audiobook)

    response = await async_client.post(
        "/ratings/",
        json={
            "user_id": user.user_id,
            "audiobook_id": audiobook.audiobook_id,
            "rating": 5,
        },
    )
    assert response.status_code == 200
    assert response.json()["rating"] == 5


@pytest.mark.asyncio
async def test_read_rating(async_client, session):
    user = User(
        username="user1", name="John Doe", email="john@example.com", password="password"
    )
    audiobook = Audiobook(
        title="Audiobook One",
        author_id=1,
        narrator_id=1,
        duration=3600,
        description="Description for audiobook one",
        release_date="2023-01-01T00:00:00",
    )
    rating = Rating(user=user, audiobook=audiobook, rating=5)
    session.add(user)
    session.add(audiobook)
    session.add(rating)
    session.commit()
    session.refresh(rating)

    response = await async_client.get(f"/ratings/{rating.rating_id}")
    assert response.status_code == 200
    assert response.json()["rating"] == 5


@pytest.mark.asyncio
async def test_list_ratings(async_client, session):
    user = User(
        username="user1", name="John Doe", email="john@example.com", password="password"
    )
    audiobook = Audiobook(
        title="Audiobook One",
        author_id=1,
        narrator_id=1,
        duration=3600,
        description="Description for audiobook one",
        release_date="2023-01-01T00:00:00",
    )
    rating1 = Rating(user=user, audiobook=audiobook, rating=5)
    rating2 = Rating(user=user, audiobook=audiobook, rating=4)
    session.add(user)
    session.add(audiobook)
    session.add(rating1)
    session.add(rating2)
    session.commit()

    response = await async_client.get("/ratings/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_rating(async_client, session):
    user = User(
        username="user1", name="John Doe", email="john@example.com", password="password"
    )
    audiobook = Audiobook(
        title="Audiobook One",
        author_id=1,
        narrator_id=1,
        duration=3600,
        description="Description for audiobook one",
        release_date="2023-01-01T00:00:00",
    )
    rating = Rating(user=user, audiobook=audiobook, rating=5)
    session.add(user)
    session.add(audiobook)
    session.add(rating)
    session.commit()
    session.refresh(rating)

    response = await async_client.put(
        f"/ratings/{rating.rating_id}",
        json={
            "user_id": user.user_id,
            "audiobook_id": audiobook.audiobook_id,
            "rating": 4,
        },
    )
    assert response.status_code == 200
    assert response.json()["rating"] == 4


@pytest.mark.asyncio
async def test_delete_rating(async_client, session):
    user = User(
        username="user1", name="John Doe", email="john@example.com", password="password"
    )
    audiobook = Audiobook(
        title="Audiobook One",
        author_id=1,
        narrator_id=1,
        duration=3600,
        description="Description for audiobook one",
        release_date="2023-01-01T00:00:00",
    )
    rating = Rating(user=user, audiobook=audiobook, rating=5)
    session.add(user)
    session.add(audiobook)
    session.add(rating)
    session.commit()
    session.refresh(rating)

    response = await async_client.delete(f"/ratings/{rating.rating_id}")
    assert response.status_code == 200
    assert response.json()["rating"] == 5
