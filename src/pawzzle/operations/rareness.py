from sqlalchemy.orm import Session

from pawzzle.db.models import Dog, DogRareness
from pawzzle.db.rareness import (
    BulkRarenessData,
    ColumnUpdateMap,
    bulk_insert_rareness,
    bulk_update_rareness,
)
from pawzzle.operations.schemas import RarenessUpdate


def seed_rareness_table(session: Session) -> None:
    rareness = session.query(DogRareness).all()
    if rareness:
        return None

    all_dogs = session.query(Dog).all()

    bulk_rareness_data: list[BulkRarenessData] = [{"id": dog.id} for dog in all_dogs]
    bulk_insert_rareness(session, bulk_rareness_data)


def update_rareness(
    session: Session, rareness_update_list: list[RarenessUpdate]
) -> None:
    rareness_update_list_json: ColumnUpdateMap = {
        r.dog_id: r.rareness.value for r in rareness_update_list
    }

    bulk_update_rareness(session, rareness_update_list_json)
