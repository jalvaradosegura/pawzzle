from sqlalchemy.orm import Session

from pawzzle.db.models import Dog, DogRareness
from pawzzle.db.rareness import BulkRarenessData, bulk_insert_rareness


def seed_rareness_table(session: Session) -> None:
    rareness = session.query(DogRareness).all()
    if rareness:
        return None

    all_dogs = session.query(Dog).all()

    bulk_rareness_data: list[BulkRarenessData] = [{"id": dog.id} for dog in all_dogs]
    bulk_insert_rareness(session, bulk_rareness_data)
