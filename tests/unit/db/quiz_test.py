import pytest
from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.db.models import Question
from pawzzle.db.question import insert_question, select_all_questions
from pawzzle.db.quiz import insert_quiz, select_all_quizzes, select_quiz


@pytest.fixture(name="seed_questions", autouse=True)
def seed_questions_fixture(session: Session) -> None:
    poodle = insert_dog(session, "Poodle")
    pug = insert_dog(session, "Pug")
    insert_question(
        session,
        text="Which one is a Poodle?",
        alternatives=[poodle, pug],
        correct_dog=poodle,
    )
    insert_question(
        session,
        text="Which one is a Pug?",
        alternatives=[poodle, pug],
        correct_dog=pug,
    )


@pytest.fixture(name="questions")
def questions_fixture(session: Session) -> list[Question]:
    return select_all_questions(session)


def test_insert_quiz(session: Session, questions: list[Question]):
    quiz = insert_quiz(session, questions, "2024-08-23")

    assert quiz.id == 1
    assert len(quiz.questions) == 2


def test_select_quiz(session: Session, questions: list[Question]):
    insert_quiz(session, questions, "2024-08-23")

    quiz = select_quiz(session, 1)

    assert quiz.id == 1
    assert len(quiz.questions) == 2


def test_get_all_quizzes(session: Session, questions: list[Question]):
    insert_quiz(session, questions, "2024-08-23")
    insert_quiz(session, questions, "2024-08-23")
    insert_quiz(session, questions, "2024-08-23")

    quizzes = select_all_quizzes(session)

    assert len(quizzes) == 3


def test_select_all_quizzes_limit(session: Session, questions: list[Question]):
    q = select_all_questions(session)
    insert_quiz(session, q, "2024-08-23")
    q = select_all_questions(session)
    insert_quiz(session, q, "2024-08-23")
    q = select_all_questions(session)
    insert_quiz(session, q, "2024-08-23")

    quizzes = select_all_quizzes(session, limit=2)

    assert len(quizzes) == 2


def test_select_all_quizzes_offset(session: Session, questions: list[Question]):
    q = select_all_questions(session)
    insert_quiz(session, q, "2024-08-23")
    q = select_all_questions(session)
    insert_quiz(session, q, "2024-08-23")
    q = select_all_questions(session)
    insert_quiz(session, q, "2024-08-23")

    quizzes = select_all_quizzes(session, offset=1)

    assert len(quizzes) == 2


def test_select_all_quizzes_limit_and_offset(
    session: Session, questions: list[Question]
):
    q = select_all_questions(session)
    insert_quiz(session, q, "2024-08-23")
    q = select_all_questions(session)
    insert_quiz(session, q, "2024-08-23")
    q = select_all_questions(session)
    insert_quiz(session, q, "2024-08-23")

    quizzes = select_all_quizzes(session, limit=1, offset=2)

    assert len(quizzes) == 1
