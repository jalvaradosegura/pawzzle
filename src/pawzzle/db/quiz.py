from sqlalchemy.orm import Session

from pawzzle.db.models import Quiz


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


def insert_quiz(session: Session, quiz: Quiz) -> Quiz:
    session.add(quiz)
    session.commit()
    return quiz


def bulk_insert_quizzes(session: Session, quizzes: list[Quiz]):
    session.add_all(quizzes)
    session.commit()
