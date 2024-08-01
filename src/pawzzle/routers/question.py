from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pawzzle.dependencies import get_session
from pawzzle.operations import question as operations
from pawzzle.operations.schemas import QuestionSchema, QuestionWithIDSchema

router = APIRouter()


@router.get("/question")
def get_random_question(
    session: Session = Depends(get_session), alternatives_amount: int = 4
) -> QuestionSchema:
    return operations.generate_random_question(
        session, alternatives_amount=alternatives_amount
    )


@router.post("/question", status_code=201)
def store_question(
    question: QuestionSchema, session: Session = Depends(get_session)
) -> QuestionWithIDSchema:
    return operations.store_question(session, question)
