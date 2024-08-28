from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.db.models import DogRareness
from pawzzle.operations.rareness import seed_rareness_table


def test_seed_rareness_table(session: Session):
    insert_dog(session, "Poodle")
    insert_dog(session, "Pug")
    insert_dog(session, "Husky")

    seed_rareness_table(session)
    rareness = session.query(DogRareness).all()

    assert len(rareness) == 3


def test_seed_rareness_table_already_seeded(session: Session):
    insert_dog(session, "Poodle")
    insert_dog(session, "Pug")
    insert_dog(session, "Husky")

    seed_rareness_table(session)
    rareness = session.query(DogRareness).all()
    seed_rareness_table(session)

    assert len(rareness) == 3
