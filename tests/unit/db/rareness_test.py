import pytest
from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.db.rareness import (
    ColumnUpdateMap,
    BulkRarenessData,
    bulk_insert_rareness,
    bulk_update_rareness,
)
from pawzzle.db.models import DogRareness


@pytest.fixture(name="prepare_data", autouse=True)
def prepare_data_fixture(session: Session):
    dog_1 = insert_dog(session, "Poodle")
    dog_2 = insert_dog(session, "Pug")
    dog_3 = insert_dog(session, "Husky")
    dog_4 = insert_dog(session, "Corgi")
    dog_5 = insert_dog(session, "Samoyed")
    dog_6 = insert_dog(session, "Golden")
    dog_rareness_1 = DogRareness(id=dog_1.id, common=10)
    dog_rareness_2 = DogRareness(id=dog_2.id)
    dog_rareness_3 = DogRareness(id=dog_3.id)
    dog_rareness_4 = DogRareness(id=dog_4.id)
    dog_rareness_5 = DogRareness(id=dog_5.id)
    dog_rareness_6 = DogRareness(id=dog_6.id)
    session.add(dog_rareness_1)
    session.add(dog_rareness_2)
    session.add(dog_rareness_3)
    session.add(dog_rareness_4)
    session.add(dog_rareness_5)
    session.add(dog_rareness_6)
    session.commit()


def test_bulk_update_rareness(session: Session):
    update_data: ColumnUpdateMap = {1: "common", 2: "uncommon"}

    bulk_update_rareness(session, update_data)
    data = session.query(DogRareness).all()

    assert len(data) == 6
    assert data[0].common == 11
    assert data[0].uncommon == 0
    assert data[0].rare == 0
    assert data[1].common == 0
    assert data[1].uncommon == 1
    assert data[1].rare == 0


def test_bulk_update_rareness_unknown_rareness(session: Session):
    update_data: ColumnUpdateMap = {1: "common", 2: "unknown"}  # type: ignore

    with pytest.raises(KeyError):
        bulk_update_rareness(session, update_data)


def test_bulk_insert_rareness(session: Session):
    dog_1 = insert_dog(session, "Fake Dog 1")
    dog_2 = insert_dog(session, "Fake Dog 2")

    rareness_data: list[BulkRarenessData] = [{"id": dog_1.id}, {"id": dog_2.id}]
    bulk_insert_rareness(session, rareness_data)
    data = session.query(DogRareness).all()

    assert len(data) == 8
