from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pawzzle.dependencies import get_session
from pawzzle.operations import answer as operations
from pawzzle.operations.schemas import AnswerIn, AnswerOut


router = APIRouter()


@router.post("/answer", status_code=201)
def store_answer(
    answer_schema: AnswerIn, session: Session = Depends(get_session)
) -> AnswerOut:
    answer = operations.store_answer(answer_schema, session)
    return answer
