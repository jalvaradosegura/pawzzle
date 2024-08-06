import pytest
from sqlalchemy.orm import Session

from pawzzle import db
from pawzzle.operations.question import generate_random_question
from pawzzle.operations.quiz import store_quiz
from pawzzle.operations.schemas import QuestionIn, QuizOut


@pytest.fixture(name="list_of_questions")
def list_of_questions_fixture(session: Session) -> list[QuestionIn]:
    db.insert_dog(session, "Poodle")
    db.insert_dog(session, "Pug")
    db.insert_dog(session, "Husky")
    question_1 = generate_random_question(session, alternatives_amount=3)
    question_2 = generate_random_question(session, alternatives_amount=3)
    question_3 = generate_random_question(session, alternatives_amount=3)
    return [question_1, question_2, question_3]


def test_store_quiz(session: Session, list_of_questions: list[QuestionIn]):
    quiz = store_quiz(session, list_of_questions)
    assert isinstance(quiz, QuizOut)
    assert len(quiz.questions) == 3
    assert len(quiz.questions[0].alternatives) == 3
