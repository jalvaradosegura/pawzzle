import pytest

from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.db.models import Question
from pawzzle.db.question import insert_question
from pawzzle.operations.answer import store_answer
from pawzzle.operations.schemas import AnswerIn


@pytest.fixture(name="question")
def question_fixture(session: Session) -> Question:
    poodle = insert_dog(session, "Poodle")
    pug = insert_dog(session, "Pug")
    insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )
    question = insert_question(
        session,
        text="Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
    )

    return question


def test_store_answer_correct(session: Session, question: Question):
    schema = AnswerIn(dog_id=2, question_id=question.id)
    answer = store_answer(session, schema)
    assert answer.correct is True


def test_store_answer_incorrect(session: Session, question: Question):
    schema = AnswerIn(dog_id=1, question_id=question.id)
    answer = store_answer(session, schema)
    assert answer.correct is False
