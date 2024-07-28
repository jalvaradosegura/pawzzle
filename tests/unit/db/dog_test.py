import pytest
from pytest import MonkeyPatch
from sqlalchemy.orm import Session, Query
from sqlalchemy.exc import NoResultFound

from pawzzle.db.dog import get_all_dogs, get_dog, store_dog, randomly_get_n_dogs
from pawzzle.db.models import Dog


def test_store_dog(session: Session):
    dog = store_dog("Poodle", session)

    assert dog.id == 1
    assert dog.breed == "Poodle"


@pytest.mark.parametrize("target_id, target_breed", [[1, "Poodle"], [2, "Pug"]])
def test_get_dog(target_id: int, target_breed: str, session: Session):
    store_dog("Poodle", session)
    store_dog("Pug", session)

    dog = get_dog(target_id, session)

    assert dog.id == target_id
    assert dog.breed == target_breed


def test_get_dog_exception(session: Session):
    with pytest.raises(NoResultFound):
        get_dog(10, session)


def test_get_all_dogs(session: Session):
    store_dog("Poodle", session)
    store_dog("Pug", session)
    store_dog("Husky", session)

    dogs = get_all_dogs(session)

    assert len(dogs) == 3


def test_get_all_dogs_limit(session: Session):
    store_dog("Poodle", session)
    store_dog("Pug", session)
    store_dog("Husky", session)

    dogs = get_all_dogs(session, limit=2)

    assert len(dogs) == 2
    assert dogs[0].breed == "Poodle"
    assert dogs[1].breed == "Pug"


def test_get_all_dogs_offset(session: Session):
    store_dog("Poodle", session)
    store_dog("Pug", session)
    store_dog("Husky", session)

    dogs = get_all_dogs(session, offset=1)

    assert len(dogs) == 2
    assert dogs[0].breed == "Pug"
    assert dogs[1].breed == "Husky"


def test_get_all_dogs_limit_and_offset(session: Session):
    store_dog("Poodle", session)
    store_dog("Pug", session)
    store_dog("Husky", session)

    dogs = get_all_dogs(session, limit=1, offset=1)

    assert len(dogs) == 1
    assert dogs[0].breed == "Pug"


def test_randomly_get_n_dogs(session: Session, monkeypatch: MonkeyPatch):
    dog_1 = store_dog("Poodle", session)
    dog_2 = store_dog("Pug", session)
    dog_3 = store_dog("Husky", session)
    store_dog("Corgi", session)
    store_dog("Samoyed", session)
    n = 3

    def mocked_query_all(query: Query[Dog]) -> list[Dog]:
        return [dog_1, dog_2, dog_3]

    monkeypatch.setattr(Query, "all", mocked_query_all)
    dogs = randomly_get_n_dogs(n, session)

    assert len(dogs) == 3
    assert dogs[0].breed == "Poodle"
