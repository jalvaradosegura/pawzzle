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


def get_quiz(id: int, session: Session) -> Quiz:
    return session.get_one(Quiz, id)


def insert_quiz(questions: list[Question], session: Session) -> Quiz:
    quiz = Quiz(questions_as_alternative=questions)
    session.add(quiz)
    session.commit()
    return quiz
