from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pawzzle import operations
from pawzzle.dependencies import get_session

router = APIRouter()


@router.post("/quiz", status_code=201)
def post_quiz(
    quiz_in: operations.QuizIn,
    session: Session = Depends(get_session),
):
    return operations.store_quiz(session, quiz_in)


@router.get("/quiz/{quiz_id}")
def get_quiz(
    quiz_id: int, session: Session = Depends(get_session)
) -> operations.QuizOut:
    return operations.get_quiz(session, quiz_id)
