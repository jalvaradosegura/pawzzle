import pytest
from sqlalchemy.orm import Session

from pawzzle.db.dog import store_dog
from pawzzle.db.models import Question
from pawzzle.db.question import get_all_questions, store_question
from pawzzle.db.quiz import get_all_quizzes, get_quiz, store_quiz


@pytest.fixture(name="seed_questions", autouse=True)
def seed_questions_fixture(session: Session) -> None:
    poodle = store_dog("Poodle", session)
    pug = store_dog("Pug", session)
    store_question(
        "Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
        session=session,
    )
    store_question(
        "Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
        session=session,
    )


@pytest.fixture(name="questions")
def questions_fixture(session: Session) -> list[Question]:
    return get_all_questions(session)


def test_store_quiz(session: Session, questions: list[Question]):
    quiz = store_quiz(questions, session)

    assert quiz.id == 1
    assert len(quiz.questions_as_alternative) == 2


def test_get_quiz(session: Session, questions: list[Question]):
    store_quiz(questions, session)

    quiz = get_quiz(1, session)

    assert quiz.id == 1
    assert len(quiz.questions_as_alternative) == 2


def test_get_all_quizzes(session: Session, questions: list[Question]):
    store_quiz(questions, session)
    store_quiz(questions, session)
    store_quiz(questions, session)

    quizzes = get_all_quizzes(session)

    assert len(quizzes) == 3


def test_get_all_quizzes_limit(session: Session, questions: list[Question]):
    q = get_all_questions(session)
    store_quiz(q, session)
    q = get_all_questions(session)
    store_quiz(q, session)
    q = get_all_questions(session)
    store_quiz(q, session)

    quizzes = get_all_quizzes(session, limit=2)

    assert len(quizzes) == 2


def test_get_all_quizzes_offset(session: Session, questions: list[Question]):
    q = get_all_questions(session)
    store_quiz(q, session)
    q = get_all_questions(session)
    store_quiz(q, session)
    q = get_all_questions(session)
    store_quiz(q, session)

    quizzes = get_all_quizzes(session, offset=1)

    assert len(quizzes) == 2


def test_get_all_quizzes_limit_and_offset(session: Session, questions: list[Question]):
    q = get_all_questions(session)
    store_quiz(q, session)
    q = get_all_questions(session)
    store_quiz(q, session)
    q = get_all_questions(session)
    store_quiz(q, session)

    quizzes = get_all_quizzes(session, limit=1, offset=2)

    assert len(quizzes) == 1
