from typing import Literal, TypedDict

from sqlalchemy import insert, inspect
from sqlalchemy.orm import Session

from pawzzle.db.models import DogRareness


ColumnUpdateMap = dict[int, Literal["common", "uncommon", "rare"]]


def bulk_update_rareness(session: Session, column_update_map: ColumnUpdateMap) -> None:

    ids_to_update: list[int] = list(column_update_map.keys())

    dogs_to_update = [
        dog_rareness.to_dict()
        for dog_rareness in (
            session.query(DogRareness).filter(DogRareness.id.in_(ids_to_update)).all()
        )
    ]

    for dog_to_update in dogs_to_update:
        rareness = column_update_map[dog_to_update["id"]]
        dog_to_update[rareness] += 1

    session.bulk_update_mappings(inspect(DogRareness), dogs_to_update)
    session.commit()


class BulkRarenessData(TypedDict):
    id: int


def bulk_insert_rareness(session: Session, rareness_data: list[BulkRarenessData]):
    session.execute(insert(DogRareness), rareness_data)
    session.commit()
