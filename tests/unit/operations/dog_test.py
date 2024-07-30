from pathlib import Path

from sqlalchemy.orm import Session

from pawzzle.db.dog import get_all_dogs
from pawzzle.operations.dog import read_dogs_from_file, store_dogs_from_file


def test_read_dogs_from_file(data_path: Path):
    dogs_data = read_dogs_from_file(data_path / "dogs.json")

    assert len(dogs_data) == 602
    assert dogs_data[0]["breed"] == "Affenpinscher"


def test_store_dogs_from_file(session: Session, data_path: Path):
    store_dogs_from_file(session, data_path / "dogs.json")

    all_dogs = get_all_dogs(session)

    assert len(all_dogs) == 602
