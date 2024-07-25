from sqlalchemy.orm import Session

from pawzzle.db.models import Dog, Question


def get_all_questions(
    session: Session, limit: None | int = None, offset: None | int = None
) -> list[Question]:
    query = session.query(Question)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)

    return query.all()


def get_question(id: int, session: Session) -> Question:
    return session.get_one(Question, id)


def store_question(
    text: str, *, alternatives: list[Dog], correct_dog: Dog, session: Session
) -> Question:
    question = Question(text=text, alternatives=alternatives, correct_dog=correct_dog)
    session.add(question)
    session.commit()
    return question
