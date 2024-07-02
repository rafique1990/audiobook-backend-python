import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import Review, User, Audiobook

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
async def test_create_review(async_client, session):
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
        "/reviews/",
        json={
            "user_id": user.user_id,
            "audiobook_id": audiobook.audiobook_id,
            "review_text": "Great audiobook!",
        },
    )
    assert response.status_code == 200
    assert response.json()["review_text"] == "Great audiobook!"


@pytest.mark.asyncio
async def test_read_review(async_client, session):
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
    review = Review(user=user, audiobook=audiobook, review_text="Great audiobook!")
    session.add(user)
    session.add(audiobook)
    session.add(review)
    session.commit()
    session.refresh(review)

    response = await async_client.get(f"/reviews/{review.review_id}")
    assert response.status_code == 200
    assert response.json()["review_text"] == "Great audiobook!"


@pytest.mark.asyncio
async def test_list_reviews(async_client, session):
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
    review1 = Review(user=user, audiobook=audiobook, review_text="Great audiobook!")
    review2 = Review(user=user, audiobook=audiobook, review_text="Not bad")
    session.add(user)
    session.add(audiobook)
    session.add(review1)
    session.add(review2)
    session.commit()

    response = await async_client.get("/reviews/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_review(async_client, session):
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
    review = Review(user=user, audiobook=audiobook, review_text="Great audiobook!")
    session.add(user)
    session.add(audiobook)
    session.add(review)
    session.commit()
    session.refresh(review)

    response = await async_client.put(
        f"/reviews/{review.review_id}",
        json={
            "user_id": user.user_id,
            "audiobook_id": audiobook.audiobook_id,
            "review_text": "Excellent audiobook!",
        },
    )
    assert response.status_code == 200
    assert response.json()["review_text"] == "Excellent audiobook!"


@pytest.mark.asyncio
async def test_delete_review(async_client, session):
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
    review = Review(user=user, audiobook=audiobook, review_text="Great audiobook!")
    session.add(user)
    session.add(audiobook)
    session.add(review)
    session.commit()
    session.refresh(review)

    response = await async_client.delete(f"/reviews/{review.review_id}")
    assert response.status_code == 200
    assert response.json()["review_text"] == "Great audiobook!"
