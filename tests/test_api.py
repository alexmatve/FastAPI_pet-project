import pytest
from httpx import AsyncClient, ASGITransport
from main import app


# pytest -vs tests/


@pytest.mark.asyncio
async def test_get_vacancies():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as ac:
        response = await ac.get("/vacancy/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5


@pytest.mark.asyncio
async def test_get_vacancy_by_id():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as ac:
        id = 1
        response = await ac.get(f"/vacancy/{id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == 1
        assert type(data["name"]) == str and len(data["name"]) > 0
        assert type(data["salary"]) == str and len(data["salary"]) > 0
        assert type(data["skills"]) == list


id_test: int


@pytest.mark.asyncio
async def test_post_vacancy():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as ac:
        response = await ac.post("/vacancy/", params={"name": "Teacher",
                                                      "salary": "40000",
                                                      "text": "Biology",
                                                      "created": "05.05.24",
                                                      })

        assert response.status_code == 200
        data = response.json()
        assert type(data["id"]) == int
        global id_test
        id_test = data["id"]
        assert data["name"] == "Teacher"
        assert data["salary"] == "40000"
        assert data["text"] == "Biology"
        assert data["created"] == "05.05.24"


@pytest.mark.asyncio
async def test_put_vacancy_by_id():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as ac:
        global id_test

        response = await ac.put(f"/vacancy/{id_test}", params={"name": "Teacher",
                                                                "salary": "40000",
                                                                "text": "History",
                                                                "created": "05.05.24",
                                                                })

        assert response.status_code == 200
        data = response.json()
        assert type(data["id"]) == int
        assert data["name"] == "Teacher"
        assert data["salary"] == "40000"
        assert data["text"] == "History"
        assert data["created"] == "05.05.24"


@pytest.mark.asyncio
async def test_delete_vacancy_by_id():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as ac:
        global id_test

        response = await ac.delete(f"/vacancy/{id_test}")

        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Teacher"
        assert data["salary"] == "40000"
        assert data["text"] == "History"
        assert data["created"] == "05.05.24"

@pytest.mark.asyncio
async def test_get_vacancies_by_skills():
    async with AsyncClient(
            transport=ASGITransport(app=app),
            base_url="http://test",
    ) as ac:
        response = await ac.get(f"/vacancy/skill/", params={"skills": ["пунктуальность", "обучаемость"]})

        assert response.status_code == 200
        data = response.json()[0]
        assert type(data["name"]) == str and len(data["name"]) > 0
        assert type(data["salary"]) == str and len(data["salary"]) > 0
        assert type(data["skills"]) == list and "пунктуальность" in data["skills"] and "обучаемость" in data["skills"]
