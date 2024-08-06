from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pawzzle.dependencies import get_session
from pawzzle.operations.schemas import QuestionIn
from pawzzle.operations import quiz as operations

router = APIRouter()


@router.post("/quiz", status_code=201)
def post_quiz(
    list_of_questions: list[QuestionIn], session: Session = Depends(get_session)
):
    return operations.store_quiz(session, list_of_questions)
