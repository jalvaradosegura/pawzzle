import random

import pytest
from pytest import MonkeyPatch
from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.db.models import Dog
from pawzzle.db.question import select_question
from pawzzle.operations.question import store_question, generate_random_question


@pytest.fixture(name="random_question", autouse=True)
def random_question_fixture(session: Session, monkeypatch: MonkeyPatch):
    dog_1 = insert_dog("Poodle", session)
    dog_2 = insert_dog("Pug", session)
    dog_3 = insert_dog("Husky", session)
    insert_dog("Corgi", session)
    insert_dog("Samoyed", session)
    random.seed(1)

    def mocked_randomly_get_n_dogs(
        alternatives_amount: int, session: Session
    ) -> list[Dog]:
        return [dog_1, dog_2, dog_3]

    monkeypatch.setattr(
        "pawzzle.operations.question.randomly_select_n_dogs",
        mocked_randomly_get_n_dogs,
    )


def test_generate_random_question(session: Session):
    question = generate_random_question(session, alternatives_amount=3)

    assert len(question.alternatives) == 3
    assert question.text == "Which one is a Poodle"
    assert question.correct_dog.breed == "Poodle"
    assert question.alternatives[0].breed == "Poodle"
    assert question.alternatives[1].breed == "Pug"
    assert question.alternatives[2].breed == "Husky"


def test_store_question(session: Session):
    question = generate_random_question(session, alternatives_amount=3)
    store_question(session, question)

    stored_question = select_question(1, session)

    assert stored_question.text == "Which one is a Poodle"
    assert stored_question.correct_dog.breed == "Poodle"
    assert stored_question.alternatives[0].breed == "Poodle"
    assert stored_question.alternatives[1].breed == "Pug"
    assert stored_question.alternatives[2].breed == "Husky"
