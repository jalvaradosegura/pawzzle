from sqlalchemy.orm import Session

from pawzzle.db.answer import insert_answer
from pawzzle.db.question import select_question
from pawzzle.operations.schemas import AnswerIn, AnswerOut


def store_answer(answer_schema: AnswerIn, session: Session) -> AnswerOut:
    question = select_question(answer_schema.question_id, session)
    is_correct = question.correct_dog_id == answer_schema.dog_id

    answer = insert_answer(
        dog_id=answer_schema.dog_id,
        correct=is_correct,
        question_id=answer_schema.question_id,
        session=session,
    )

    return AnswerOut(**answer.to_dict())
