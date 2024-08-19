from datetime import datetime
from unittest.mock import MagicMock, Mock, patch

import pytest
from fastapi import BackgroundTasks
from sqlalchemy.orm import Session

from pawzzle import db
from pawzzle.db.question import BulkQuestionData
from pawzzle.operations.question import generate_random_question, store_questions
from pawzzle.operations.quiz import (
    generate_random_quiz,
    get_quiz,
    get_quiz_by_date,
    get_todays_quiz,
    seed_quiz_table,
    store_quiz,
)
from pawzzle.operations.schemas import QuestionIn, QuizIn, QuizOut
from tests.fakes.cache import CacheFake


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
    quiz_in = QuizIn(questions=list_of_questions, target_date="2024-08-23")

    quiz = store_quiz(session, quiz_in)

    assert isinstance(quiz, QuizOut)
    assert len(quiz.questions) == 3
    assert len(quiz.questions[0].alternatives) == 3
    assert len(quiz.questions[1].alternatives) == 3
    assert len(quiz.questions[2].alternatives) == 3


def test_store_quiz_directly_use_db(
    session: Session, list_of_questions: list[QuestionIn]
):
    store_questions(session, list_of_questions)
    questions = db.select_all_questions(session)

    quiz = db.Quiz(questions=questions, target_date="2024-08-23")
    db.insert_quiz(session, quiz)
    quiz = db.Quiz(questions=questions, target_date="2024-08-23")
    db.insert_quiz(session, quiz)
    quiz = db.select_quiz(session, 1)
    associations = session.query(db.quiz_question_association).all()
    questions = db.select_all_questions(session)

    assert len(quiz.questions) == 3
    assert quiz.target_date == "2024-08-23"
    assert len(associations) == 6
    assert len(questions) == 3


def test_get_quiz(session: Session, list_of_questions: list[QuestionIn]):
    quiz_in = QuizIn(questions=list_of_questions, target_date="2024-08-23")
    store_quiz(session, quiz_in)

    quiz = get_quiz(session, 1)

    assert isinstance(quiz, QuizOut)
    assert len(quiz.questions) == 3
    assert len(quiz.questions[0].alternatives) == 3
    assert len(quiz.questions[1].alternatives) == 3
    assert len(quiz.questions[2].alternatives) == 3


def test_get_quiz_by_date(session: Session, list_of_questions: list[QuestionIn]):
    quiz_in = QuizIn(questions=list_of_questions, target_date="2024-08-23")
    store_quiz(session, quiz_in)

    quiz = get_quiz_by_date(session, "2024-08-23")

    assert isinstance(quiz, QuizOut)
    assert len(quiz.questions) == 3
    assert len(quiz.questions[0].alternatives) == 3
    assert len(quiz.questions[1].alternatives) == 3
    assert len(quiz.questions[2].alternatives) == 3


@patch("pawzzle.operations.quiz.datetime")
def test_get_todays_quiz(
    mocked_datetime_now: MagicMock,
    session: Session,
    list_of_questions: list[QuestionIn],
):
    mocked_datetime_now.now = Mock(return_value=datetime(2024, 8, 23))
    quiz_in = QuizIn(questions=list_of_questions, target_date="2024-08-23")
    store_quiz(session, quiz_in)

    quiz = get_todays_quiz(CacheFake(), session, BackgroundTasks())

    assert isinstance(quiz, QuizOut)
    assert quiz.target_date == "2024-08-23"
    assert len(quiz.questions) == 3
    assert len(quiz.questions[0].alternatives) == 3
    assert len(quiz.questions[1].alternatives) == 3
    assert len(quiz.questions[2].alternatives) == 3


@patch("pawzzle.operations.quiz.datetime")
def test_get_todays_quiz_cached(
    mocked_datetime_now: MagicMock,
    session: Session,
    list_of_questions: list[QuestionIn],
):
    mocked_datetime_now.now = Mock(return_value=datetime(2024, 8, 23))
    quiz_in = QuizIn(questions=list_of_questions, target_date="2024-08-23")
    store_quiz(session, quiz_in)
    cache_fake = CacheFake()
    background_tasks = BackgroundTasks()

    get_todays_quiz(cache_fake, session, background_tasks)
    # Manually execute the background task
    for task in background_tasks.tasks:
        task.func(*task.args, **task.kwargs)
    quiz = get_todays_quiz(cache_fake, session, background_tasks)

    assert isinstance(quiz, QuizOut)
    assert quiz.target_date == "2024-08-23"
    assert len(quiz.questions) == 3
    assert len(quiz.questions[0].alternatives) == 3
    assert len(quiz.questions[1].alternatives) == 3
    assert len(quiz.questions[2].alternatives) == 3


def test_generate_random_quiz(
    session: Session,
    list_of_questions: list[QuestionIn],
):
    bulk_data: list[BulkQuestionData] = [
        {
            "text": q.text,
            "correct_dog_id": q.correct_dog.id,
            "alternatives": [a.id for a in q.alternatives],
        }
        for q in list_of_questions
    ]
    db.bulk_insert_questions(session, bulk_data)

    quiz = generate_random_quiz(session, questions_amount=5, target_date="2024-08-23")
    questions = db.select_all_questions(session)

    assert isinstance(quiz, QuizIn)
    assert quiz.target_date == "2024-08-23"
    assert len(questions) == 3
    assert len(questions[0].alternatives) == 3
    assert len(questions[1].alternatives) == 3
    assert len(questions[2].alternatives) == 3


def test_seed_quiz_table(
    session: Session,
    list_of_questions: list[QuestionIn],
):
    bulk_data: list[BulkQuestionData] = [
        {
            "text": q.text,
            "correct_dog_id": q.correct_dog.id,
            "alternatives": [a.id for a in q.alternatives],
        }
        for q in list_of_questions
    ]
    db.bulk_insert_questions(session, bulk_data)

    seed_quiz_table(session, year=2024, questions_per_quiz=3)
    quizzes = db.select_all_quizzes(session)
    questions = db.select_all_questions(session)
    associations = session.query(db.quiz_question_association).all()

    assert len(quizzes) == 366
    assert len(questions) == 3
    assert len(associations) == 1098


def test_seed_quiz_table_already_seeded(
    session: Session,
    list_of_questions: list[QuestionIn],
):
    bulk_data: list[BulkQuestionData] = [
        {
            "text": q.text,
            "correct_dog_id": q.correct_dog.id,
            "alternatives": [a.id for a in q.alternatives],
        }
        for q in list_of_questions
    ]
    db.bulk_insert_questions(session, bulk_data)
    quiz = generate_random_quiz(session, questions_amount=5, target_date="2024-01-01")
    store_quiz(session, quiz)

    seed_quiz_table(session, year=2024, questions_per_quiz=3)
    quizzes = db.select_all_quizzes(session)

    assert len(quizzes) == 1
