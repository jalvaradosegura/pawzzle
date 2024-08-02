from sqlalchemy.orm import Session

from pawzzle.db.answer import insert_answer
from pawzzle.db.question import select_question
from pawzzle.operations.schemas import AnswerIn, AnswerOut


def store_answer(session: Session, answer_schema: AnswerIn) -> AnswerOut:
    question = select_question(session, answer_schema.question_id)
    is_correct = question.correct_dog_id == answer_schema.dog_id

    answer = insert_answer(
        session,
        dog_id=answer_schema.dog_id,
        correct=is_correct,
        question_id=answer_schema.question_id,
    )

    return AnswerOut(**answer.to_dict())
