import pytest
from sqlalchemy.orm import Session

from pawzzle.db.answer import insert_answer
from pawzzle.db.dog import insert_dog
from pawzzle.db.models import Question
from pawzzle.db.question import insert_question


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


def test_insert_answer(session: Session, question: Question):
    answer = insert_answer(session, dog_id=2, correct=True, question_id=question.id)

    assert answer.id == 1
    assert answer.correct is True
    assert answer.question_id == 2
    assert answer.question.text == "Which one is a Pug?"
    assert answer.dog.breed == "Pug"
