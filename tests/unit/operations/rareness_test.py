from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.db.models import DogRareness
from pawzzle.operations.rareness import seed_rareness_table, update_rareness
from pawzzle.operations.schemas import Rareness, RarenessUpdate


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


def test_update_rareness(session: Session):
    dog_1 = insert_dog(session, "Poodle")
    dog_2 = insert_dog(session, "Setter")
    dog_3 = insert_dog(session, "Fila")
    dog_rareness_1 = DogRareness(id=dog_1.id)
    dog_rareness_2 = DogRareness(id=dog_2.id)
    dog_rareness_3 = DogRareness(id=dog_3.id)
    session.add(dog_rareness_1)
    session.add(dog_rareness_2)
    session.add(dog_rareness_3)
    session.commit()
    rareness_update_list = [
        RarenessUpdate(dog_id=dog_1.id, rareness=Rareness.COMMON),
        RarenessUpdate(dog_id=dog_2.id, rareness=Rareness.UNCOMMON),
        RarenessUpdate(dog_id=dog_3.id, rareness=Rareness.RARE),
    ]

    update_rareness(session, rareness_update_list)
    rareness = (
        session.query(DogRareness)
        .where(DogRareness.id.in_([dog_1.id, dog_2.id, dog_3.id]))
        .order_by(DogRareness.id.asc())
        .all()
    )

    assert len(rareness) == 3
    assert rareness[0].common == 1
    assert rareness[0].uncommon == 0
    assert rareness[0].rare == 0
    assert rareness[1].common == 0
    assert rareness[1].uncommon == 1
    assert rareness[1].rare == 0
    assert rareness[2].common == 0
    assert rareness[2].uncommon == 0
    assert rareness[2].rare == 1
