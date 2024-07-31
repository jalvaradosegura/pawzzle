import json
from pathlib import Path

from sqlalchemy.orm import Session

from pawzzle.db.dog import BulkDogData, bulk_insert_dogs, select_all_dogs


def read_dogs_from_file(file_path: Path) -> list[BulkDogData]:
    with open(file_path) as file:
        dogs_data = json.load(file)

    return dogs_data


def insert_dogs_from_file(session: Session, dogs_data_path: Path) -> None:
    dogs_data = read_dogs_from_file(dogs_data_path)
    bulk_insert_dogs(session, dogs_data)


def seed_dog_table(session: Session, dogs_data_path: Path) -> None:
    dog = select_all_dogs(session, limit=1)
    if dog:
        return None

    insert_dogs_from_file(session, dogs_data_path)
