import json
from pathlib import Path

from sqlalchemy.orm import Session

from pawzzle import db


def read_dogs_from_file(file_path: Path) -> list[db.BulkDogData]:
    with open(file_path) as file:
        dogs_data = json.load(file)

    return dogs_data


def insert_dogs_from_file(session: Session, dogs_data_path: Path) -> None:
    dogs_data = read_dogs_from_file(dogs_data_path)
    db.bulk_insert_dogs(session, dogs_data)


def seed_dog_table(session: Session, dogs_data_path: Path) -> None:
    dog = db.select_all_dogs(session, limit=1)
    if dog:
        return None

    insert_dogs_from_file(session, dogs_data_path)
