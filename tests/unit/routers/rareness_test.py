from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pawzzle import db
from pawzzle.operations.schemas import Rareness, RarenessUpdate


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


def test_update_dogs(client: TestClient, session: Session):
    dog_1 = db.insert_dog(session, "Poodle")
    dog_2 = db.insert_dog(session, "Setter")
    dog_3 = db.insert_dog(session, "Fila")
    dog_rareness_1 = db.DogRareness(id=dog_1.id)
    dog_rareness_2 = db.DogRareness(id=dog_2.id)
    dog_rareness_3 = db.DogRareness(id=dog_3.id)
    session.add(dog_rareness_1)
    session.add(dog_rareness_2)
    session.add(dog_rareness_3)
    session.commit()
    rareness_update_list = [
        RarenessUpdate(dog_id=dog_1.id, rareness=Rareness.COMMON),
        RarenessUpdate(dog_id=dog_2.id, rareness=Rareness.UNCOMMON),
        RarenessUpdate(dog_id=dog_3.id, rareness=Rareness.RARE),
    ]

    response = client.put("/dogs", json=[r.model_dump() for r in rareness_update_list])
    rareness = (
        session.query(db.DogRareness)
        .where(db.DogRareness.id.in_([dog_1.id, dog_2.id, dog_3.id]))
        .order_by(db.DogRareness.id.asc())
        .all()
    )

    assert response.status_code == 200
    assert len(rareness) == 3
    assert rareness[0].common == 1
    assert rareness[0].uncommon == 0
    assert rareness[0].rare == 0
    assert rareness[1].common == 0
    assert rareness[1].uncommon == 1
    assert rareness[1].rare == 0
    assert rareness[2].common == 0
    assert rareness[2].uncommon == 0
    assert rareness[2].rare == 1
