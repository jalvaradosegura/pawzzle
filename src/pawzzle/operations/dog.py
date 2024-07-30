import json
from pathlib import Path

from sqlalchemy.orm import Session

from pawzzle.db.dog import BulkDogData, bulk_store_dogs


def read_dogs_from_file(file_path: Path) -> list[BulkDogData]:
    with open(file_path) as file:
        dogs_data = json.load(file)

    return dogs_data


def store_dogs_from_file(session: Session, dogs_data_path: Path):
    dogs_data = read_dogs_from_file(dogs_data_path)
    bulk_store_dogs(session, dogs_data)
