import random

import pytest
from pytest import MonkeyPatch
from sqlalchemy.orm import Session

from pawzzle import db
from pawzzle.operations.question import (
    generate_random_question,
    seed_question_table,
    store_question,
    store_questions,
)


@pytest.fixture(name="random_question", autouse=True)
def random_question_fixture(session: Session, monkeypatch: MonkeyPatch):
    dog_1 = db.insert_dog(session, "Poodle")
    dog_2 = db.insert_dog(session, "Pug")
    dog_3 = db.insert_dog(session, "Husky")
    db.insert_dog(session, "Corgi")
    db.insert_dog(session, "Samoyed")
    random.seed(1)

    def mocked_randomly_get_n_dogs(
        alternatives_amount: int, session: Session
    ) -> list[db.Dog]:
        return [dog_1, dog_2, dog_3]

    monkeypatch.setattr(
        "pawzzle.operations.question.db.randomly_select_n_dogs",
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

    stored_question = db.select_question(session, 1)

    assert stored_question.text == "Which one is a Poodle"
    assert stored_question.correct_dog.breed == "Poodle"
    assert stored_question.alternatives[0].breed == "Poodle"
    assert stored_question.alternatives[1].breed == "Pug"
    assert stored_question.alternatives[2].breed == "Husky"


def test_store_questions(session: Session) -> None:
    question_1 = generate_random_question(session, alternatives_amount=3)
    question_2 = generate_random_question(session, alternatives_amount=3)
    question_3 = generate_random_question(session, alternatives_amount=3)

    store_questions(session, [question_1, question_2, question_3])
    all_questions = db.select_all_questions(session)

    assert len(all_questions) == 3


def test_seed_question_table(session: Session):
    seed_question_table(session, questions_amount=20, alternatives_amount=4)
    questions = db.select_all_questions(session)

    assert len(questions) == 20
