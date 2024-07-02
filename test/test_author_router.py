import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import Author

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
async def test_create_author(async_client):
    response = await async_client.post(
        "/authors/", json={"name": "Author One", "bio": "Bio for Author One"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Author One"


@pytest.mark.asyncio
async def test_read_author(async_client, session):
    author = Author(name="Author One", bio="Bio for Author One")
    session.add(author)
    session.commit()
    session.refresh(author)

    response = await async_client.get(f"/authors/{author.author_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Author One"


@pytest.mark.asyncio
async def test_list_authors(async_client, session):
    author1 = Author(name="Author One", bio="Bio for Author One")
    author2 = Author(name="Author Two", bio="Bio for Author Two")
    session.add(author1)
    session.add(author2)
    session.commit()

    response = await async_client.get("/authors/")
    assert response.status_code == 200
    assert len(response.json()) == 2


@pytest.mark.asyncio
async def test_update_author(async_client, session):
    author = Author(name="Author One", bio="Bio for Author One")
    session.add(author)
    session.commit()
    session.refresh(author)

    response = await async_client.put(
        f"/authors/{author.author_id}",
        json={"name": "Updated Author", "bio": "Updated Bio"},
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Author"


@pytest.mark.asyncio
async def test_delete_author(async_client, session):
    author = Author(name="Author One", bio="Bio for Author One")
    session.add(author)
    session.commit()
    session.refresh(author)

    response = await async_client.delete(f"/authors/{author.author_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Author One"
