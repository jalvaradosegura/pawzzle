import pytest

from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.db.models import Question
from pawzzle.db.question import insert_question
from pawzzle.operations.answer import store_answer
from pawzzle.operations.schemas import AnswerIn


@pytest.fixture(name="question")
def question_fixture(session: Session) -> Question:
    poodle = insert_dog("Poodle", session)
    pug = insert_dog("Pug", session)
    insert_question(
        "Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
        session=session,
    )
    question = insert_question(
        "Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
        session=session,
    )

    return question


def test_store_answer_correct(session: Session, question: Question):
    schema = AnswerIn(dog_id=2, question_id=question.id)
    answer = store_answer(schema, session=session)
    assert answer.correct is True


def test_store_answer_incorrect(session: Session, question: Question):
    schema = AnswerIn(dog_id=1, question_id=question.id)
    answer = store_answer(schema, session=session)
    assert answer.correct is False
