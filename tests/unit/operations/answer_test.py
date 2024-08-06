import pytest

from sqlalchemy.orm import Session

from pawzzle import db

from pawzzle.operations.answer import store_answer
from pawzzle.operations.schemas import AnswerIn


@pytest.fixture(name="question")
def question_fixture(session: Session) -> db.Question:
    poodle = db.insert_dog(session, "Poodle")
    pug = db.insert_dog(session, "Pug")
    db.insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )
    question = db.insert_question(
        session,
        text="Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
    )

    return question


def test_store_answer_correct(session: Session, question: db.Question):
    schema = AnswerIn(dog_id=2, question_id=question.id)
    answer = store_answer(session, schema)
    assert answer.correct is True


def test_store_answer_incorrect(session: Session, question: db.Question):
    schema = AnswerIn(dog_id=1, question_id=question.id)
    answer = store_answer(session, schema)
    assert answer.correct is False
