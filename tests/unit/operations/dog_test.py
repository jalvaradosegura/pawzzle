from pathlib import Path

from sqlalchemy.orm import Session

from pawzzle.db.dog import select_all_dogs
from pawzzle.operations.dog import (
    insert_dogs_from_file,
    read_dogs_from_file,
    seed_dog_table,
)


def test_read_dogs_from_file(data_path: Path):
    dogs_data = read_dogs_from_file(data_path / "dogs.json")

    assert len(dogs_data) == 602
    assert dogs_data[0]["breed"] == "Affenpinscher"


def test_store_dogs_from_file(session: Session, data_path: Path):
    insert_dogs_from_file(session, data_path / "dogs.json")

    all_dogs = select_all_dogs(session)

    assert len(all_dogs) == 602


def test_seed_dog_table(session: Session, data_path: Path):
    seed_dog_table(session, data_path / "dogs.json")
    all_dogs = select_all_dogs(session)

    assert len(all_dogs) == 602


def test_seed_dog_table_already_seeded(session: Session, data_path: Path):
    seed_dog_table(session, data_path / "dogs.json")
    seed_dog_table(session, data_path / "dogs.json")
    all_dogs = select_all_dogs(session)

    assert len(all_dogs) == 602
