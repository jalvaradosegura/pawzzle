from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pawzzle import operations
from pawzzle.dependencies import get_session

router = APIRouter()


@router.post("/answer", status_code=201)
def post_answer(
    answer_schema: operations.AnswerIn, session: Session = Depends(get_session)
) -> operations.AnswerOut:
    return operations.store_answer(session, answer_schema)


@router.post("/answers", status_code=201)
def post_answers(
    answers_schema: operations.AnswersIn, session: Session = Depends(get_session)
):
    for answer_schema in answers_schema.answers:
        operations.store_answer(session, answer_schema)
