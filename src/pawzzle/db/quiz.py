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


def insert_quiz(session: Session, questions: list[Question]) -> Quiz:
    quiz = Quiz(questions=questions)
    session.add(quiz)
    session.commit()
    return quiz
