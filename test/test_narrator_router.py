import pytest
from httpx import AsyncClient
from sqlmodel import SQLModel, create_engine, Session
from main import app
from schema import Narrator

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
async def test_create_narrator(async_client):
    response = await async_client.post("/narrators/", json={
        "name": "Narrator One",
        "bio": "Bio of Narrator One"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Narrator One"

@pytest.mark.asyncio
async def test_read_narrator(async_client, session):
    narrator = Narrator(name="Narrator One", bio="Bio of Narrator One")
    session.add(narrator)
    session.commit()
    session.refresh(narrator)

    response = await async_client.get(f"/narrators/{narrator.narrator_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Narrator One"

@pytest.mark.asyncio
async def test_list_narrators(async_client, session):
    narrator1 = Narrator(name="Narrator One", bio="Bio of Narrator One")
    narrator2 = Narrator(name="Narrator Two", bio="Bio of Narrator Two")
    session.add(narrator1)
    session.add(narrator2)
    session.commit()

    response = await async_client.get("/narrators/")
    assert response.status_code == 200
    assert len(response.json()) == 2

@pytest.mark.asyncio
async def test_update_narrator(async_client, session):
    narrator = Narrator(name="Narrator One", bio="Bio of Narrator One")
    session.add(narrator)
    session.commit()
    session.refresh(narrator)

    response = await async_client.put(f"/narrators/{narrator.narrator_id}", json={
        "name": "Updated Narrator One",
        "bio": "Updated bio of Narrator One"
    })
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Narrator One"

@pytest.mark.asyncio
async def test_delete_narrator(async_client, session):
    narrator = Narrator(name="Narrator One", bio="Bio of Narrator One")
    session.add(narrator)
    session.commit()
    session.refresh(narrator)

    response = await async_client.delete(f"/narrators/{narrator.narrator_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Narrator One"
