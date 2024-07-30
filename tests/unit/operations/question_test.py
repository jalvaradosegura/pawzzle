import random
from pytest import MonkeyPatch
from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.db.models import Dog
from pawzzle.operations.question import generate_random_question


def test_generate_random_question(session: Session, monkeypatch: MonkeyPatch):
    def mocked_randomly_get_n_dogs(
        alternatives_amount: int, session: Session
    ) -> list[Dog]:
        return [dog_1, dog_2, dog_3]

    monkeypatch.setattr(
        "pawzzle.operations.question.db_dog.randomly_select_n_dogs",
        mocked_randomly_get_n_dogs,
    )
    dog_1 = insert_dog("Poodle", session)
    dog_2 = insert_dog("Pug", session)
    dog_3 = insert_dog("Husky", session)
    insert_dog("Corgi", session)
    insert_dog("Samoyed", session)
    random.seed(1)

    question = generate_random_question(session, alternatives_amount=3)

    assert len(question.alternatives) == 3
    assert question.text == "Which one is a Poodle"
    assert question.correct_dog.breed == "Poodle"
    assert question.alternatives[0].breed == "Poodle"
    assert question.alternatives[1].breed == "Pug"
    assert question.alternatives[2].breed == "Husky"
