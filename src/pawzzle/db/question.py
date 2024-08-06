from typing import TypedDict

from sqlalchemy import insert
from sqlalchemy.orm import Session

from pawzzle.db.models import Dog, Question, question_dog_association


def insert_question(
    session: Session, *, text: str, alternatives: list[Dog], correct_dog: Dog
) -> Question:
    question = Question(text=text, alternatives=alternatives, correct_dog=correct_dog)
    session.add(question)
    session.commit()
    return question


def select_all_questions(
    session: Session,
    *,
    limit: None | int = None,
    offset: None | int = None,
    filter_: list[int] | set[int] | None = None,
) -> list[Question]:
    query = session.query(Question)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    if filter_:
        query = query.where(Question.id.in_(filter_))

    return query.all()


def select_question(session: Session, id: int) -> Question:
    return session.get_one(Question, id)


class BulkQuestionData(TypedDict):
    text: str
    correct_dog_id: int
    alternatives: list[int]


class AssociationData(TypedDict):
    question_id: int
    dog_id: int


def bulk_insert_questions(
    session: Session, questions_data: list[BulkQuestionData]
) -> list[int]:
    stmt = insert(Question).values(
        [
            {"text": data["text"], "correct_dog_id": data["correct_dog_id"]}
            for data in questions_data
        ]
    )

    result = session.execute(stmt.returning(Question.id))
    inserted_ids = [row[0] for row in result]

    association_data: list[AssociationData] = []
    for idx, question in enumerate(questions_data):
        for alternative in question["alternatives"]:
            association_data.append(
                {"question_id": inserted_ids[idx], "dog_id": alternative}
            )

    session.execute(insert(question_dog_association), association_data)
    session.commit()

    return inserted_ids
