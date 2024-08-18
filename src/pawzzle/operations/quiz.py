import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from pawzzle import db
from pawzzle.cache.quiz import get_todays_quiz_if_cached, store_todays_quiz_in_cache
from pawzzle.cache.types import Cache
from pawzzle.operations.schemas import QuestionIn, QuestionOut, QuizIn, QuizOut


def store_quiz(session: Session, quiz_in: QuizIn) -> QuizOut:
    questions_to_bulk: list[db.BulkQuestionData] = [
        {
            "text": question.text,
            "alternatives": [alternative.id for alternative in question.alternatives],
            "correct_dog_id": question.correct_dog.id,
        }
        for question in quiz_in.questions
    ]
    questions_id = db.bulk_insert_questions(session, questions_to_bulk)
    questions = db.select_all_questions(session, filter_=questions_id)
    quiz = db.insert_quiz(
        session, db.Quiz(questions=questions, target_date=quiz_in.target_date)
    )

    return QuizOut(
        id=quiz.id,
        questions=[QuestionOut(**q.to_dict()) for q in quiz.questions],
        target_date=quiz_in.target_date,
    )


def get_quiz(session: Session, id: int) -> QuizOut:
    quiz = db.select_quiz(session, id)
    return QuizOut(
        id=quiz.id,
        questions=[QuestionOut(**q.to_dict()) for q in quiz.questions],
        target_date=quiz.target_date,
    )


def get_quiz_by_date(session: Session, date: str) -> QuizOut:
    quiz = db.select_quiz_by_date(session, date)
    return QuizOut(
        id=quiz.id,
        questions=[QuestionOut(**q.to_dict()) for q in quiz.questions],
        target_date=quiz.target_date,
    )


def get_todays_quiz(cache: Cache, session: Session) -> QuizOut:
    todays_date = datetime.now().strftime("%Y-%m-%d")
    if quiz := get_todays_quiz_if_cached(cache, todays_date):
        return QuizOut(**quiz)

    quiz = get_quiz_by_date(session, todays_date)

    store_todays_quiz_in_cache(cache, quiz.model_dump(), todays_date)

    return quiz


def generate_random_quiz(
    session: Session, *, questions_amount: int, target_date: str
) -> QuizIn:
    questions = db.randomly_select_n_questions(session, questions_amount)
    questions_in = [QuestionIn(**q.to_dict()) for q in questions]
    return QuizIn(target_date=target_date, questions=questions_in)


def seed_quiz_table(session: Session, *, year: int, questions_per_quiz: int = 10):
    start_date = datetime(year, 1, 1)
    start_date_str = start_date.strftime("%Y-%m-%d")

    quizzes = session.query(db.Quiz).where(db.Quiz.target_date == start_date_str).all()
    if quizzes:
        return

    quizzes: list[db.Quiz] = []
    amount_of_days_in_year = 365 if not year % 4 == 0 else 366
    all_questions = db.select_all_questions(session)
    for i in range(amount_of_days_in_year):
        current_date = start_date + timedelta(days=i)
        current_date_str = current_date.strftime("%Y-%m-%d")
        questions = random.sample(all_questions, questions_per_quiz)
        quiz = db.Quiz(target_date=current_date_str, questions=questions)
        quizzes.append(quiz)

    db.bulk_insert_quizzes(session, quizzes)
