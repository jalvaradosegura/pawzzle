from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pawzzle import db


def test_get_dogs(client: TestClient, session: Session):
    db.insert_dog(session, "Husky")
    db.insert_dog(session, "Corgi")
    db.insert_dog(session, "Samoyed")

    response = client.get("/dogs?size=1")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "items": [
            {
                "breed": "Husky",
                "id": 1,
                "img_name": None,
                "info_url": None,
            }
        ],
        "page": 1,
        "pages": 3,
        "size": 1,
        "total": 3,
    }

    response = client.get("/dogs?size=1&page=2")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "items": [
            {
                "breed": "Corgi",
                "id": 2,
                "img_name": None,
                "info_url": None,
            }
        ],
        "page": 2,
        "pages": 3,
        "size": 1,
        "total": 3,
    }

    response = client.get("/dogs?size=1&page=3")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "items": [
            {
                "breed": "Samoyed",
                "id": 3,
                "img_name": None,
                "info_url": None,
            }
        ],
        "page": 3,
        "pages": 3,
        "size": 1,
        "total": 3,
    }

    response = client.get("/dogs?size=1&page=4")
    data = response.json()

    assert response.status_code == 200
    assert data == {
        "items": [],
        "page": 4,
        "pages": 3,
        "size": 1,
        "total": 3,
    }
