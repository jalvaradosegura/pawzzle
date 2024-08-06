from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pawzzle.dependencies import get_session
from pawzzle import operations


router = APIRouter()


@router.post("/answer", status_code=201)
def post_answer(
    answer_schema: operations.AnswerIn, session: Session = Depends(get_session)
) -> operations.AnswerOut:
    answer = operations.store_answer(session, answer_schema)
    return answer
