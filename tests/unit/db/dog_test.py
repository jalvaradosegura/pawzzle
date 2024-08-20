import pytest
from pytest import MonkeyPatch
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Query, Session

from pawzzle.db.dog import (
    bulk_insert_dogs,
    insert_dog,
    randomly_select_n_dogs,
    select_all_dogs,
    select_dog,
)
from pawzzle.db.models import Dog


def test_insert_dog(session: Session):
    dog = insert_dog(session, "Poodle")

    assert dog.id == 1
    assert dog.breed == "Poodle"


@pytest.mark.parametrize("target_id, target_breed", [[1, "Poodle"], [2, "Pug"]])
def test_select_dog(target_id: int, target_breed: str, session: Session):
    insert_dog(session, "Poodle")
    insert_dog(session, "Pug")

    dog = select_dog(session, target_id)

    assert dog.id == target_id
    assert dog.breed == target_breed


def test_select_dog_exception(session: Session):
    with pytest.raises(NoResultFound):
        select_dog(session, 10)


def test_get_all_dogs(session: Session):
    insert_dog(session, "Poodle")
    insert_dog(session, "Pug")
    insert_dog(session, "Husky")

    dogs = select_all_dogs(session)

    assert len(dogs) == 3


def test_select_all_dogs_limit(session: Session):
    insert_dog(session, "Poodle")
    insert_dog(session, "Pug")
    insert_dog(session, "Husky")

    dogs = select_all_dogs(session, limit=2)

    assert len(dogs) == 2
    assert dogs[0].breed == "Poodle"
    assert dogs[1].breed == "Pug"


def test_select_all_dogs_offset(session: Session):
    insert_dog(session, "Poodle")
    insert_dog(session, "Pug")
    insert_dog(session, "Husky")

    dogs = select_all_dogs(session, offset=1)

    assert len(dogs) == 2
    assert dogs[0].breed == "Pug"
    assert dogs[1].breed == "Husky"


def test_select_all_dogs_filter(session: Session):
    insert_dog(session, "Poodle")
    insert_dog(session, "Pug")
    insert_dog(session, "Husky")
    insert_dog(session, "Corgi Pembroke")
    insert_dog(session, "Corgi Cardigan")
    insert_dog(session, "Golden")

    dogs = select_all_dogs(session, filter_={1, 2, 4})

    assert len(dogs) == 3
    assert dogs[0].breed == "Poodle"
    assert dogs[1].breed == "Pug"
    assert dogs[2].breed == "Corgi Pembroke"


def test_select_all_dogs_limit_and_offset(session: Session):
    insert_dog(session, "Poodle")
    insert_dog(session, "Pug")
    insert_dog(session, "Husky")

    dogs = select_all_dogs(session, limit=1, offset=1)

    assert len(dogs) == 1
    assert dogs[0].breed == "Pug"


def test_randomly_select_n_dogs(session: Session, monkeypatch: MonkeyPatch):
    dog_1 = insert_dog(session, "Poodle")
    dog_2 = insert_dog(session, "Pug")
    dog_3 = insert_dog(session, "Husky")
    insert_dog(session, "Corgi")
    insert_dog(session, "Samoyed")
    n = 3

    def mocked_query_all(query: Query[Dog]) -> list[Dog]:
        return [dog_1, dog_2, dog_3]

    monkeypatch.setattr(Query, "all", mocked_query_all)
    dogs = randomly_select_n_dogs(session, n)

    assert len(dogs) == 3
    assert dogs[0].breed == "Poodle"


def test_bulk_insert_dogs(session: Session):
    bulk_insert_dogs(
        session,
        [
            {
                "breed": "Affenpinscher",
                "info_url": "https://en.wikipedia.org/wiki/Affenpinscher",
                "img_name": "",
            },
            {
                "breed": "Afghan Hound",
                "info_url": "https://en.wikipedia.org/wiki/Afghan_Hound",
                "img_name": "",
            },
            {
                "breed": "Africanis",
                "info_url": "https://en.wikipedia.org/wiki/Africanis",
                "img_name": "",
            },
            {
                "breed": "Alaskan Malamute",
                "info_url": "https://en.wikipedia.org/wiki/Alaskan_Malamute",
                "img_name": "",
            },
            {
                "breed": "Alopekis",
                "info_url": "https://en.wikipedia.org/wiki/Alopekis",
                "img_name": "",
            },
        ],
    )

    dogs = select_all_dogs(session)

    assert len(dogs) == 5
