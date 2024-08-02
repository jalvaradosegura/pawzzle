from sqlalchemy.orm import Session

from pawzzle.db.models import Dog, Question


def insert_question(
    session: Session, *, text: str, alternatives: list[Dog], correct_dog: Dog
) -> Question:
    question = Question(text=text, alternatives=alternatives, correct_dog=correct_dog)
    session.add(question)
    session.commit()
    return question


def select_all_questions(
    session: Session, *, limit: None | int = None, offset: None | int = None
) -> list[Question]:
    query = session.query(Question)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)

    return query.all()


def select_question(session: Session, id: int) -> Question:
    return session.get_one(Question, id)
