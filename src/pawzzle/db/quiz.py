from sqlalchemy.orm import Session

from pawzzle.db.models import Question, Quiz


def select_all_quizzes(
    session: Session, limit: None | int = None, offset: None | int = None
) -> list[Quiz]:
    query = session.query(Quiz)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)

    return query.all()


def select_quiz(session: Session, id: int) -> Quiz:
    return session.get_one(Quiz, id)


def select_quiz_by_date(session: Session, date: str):
    return session.query(Quiz).filter(Quiz.target_date == date).one()


def insert_quiz(session: Session, questions: list[Question], target_date: str) -> Quiz:
    quiz = Quiz(questions=questions, target_date=target_date)
    session.add(quiz)
    session.commit()
    return quiz
