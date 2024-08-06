from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pawzzle import operations
from pawzzle.dependencies import get_session

router = APIRouter()


@router.post("/quiz", status_code=201)
def post_quiz(
    list_of_questions: list[operations.QuestionIn],
    session: Session = Depends(get_session),
):
    return operations.store_quiz(session, list_of_questions)
