from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pawzzle import operations
from pawzzle.dependencies import get_session

router = APIRouter()


@router.get("/question")
def get_random_question(
    session: Session = Depends(get_session), alternatives_amount: int = 4
) -> operations.QuestionIn:
    return operations.generate_random_question(
        session, alternatives_amount=alternatives_amount
    )


@router.post("/question", status_code=201)
def post_question(
    question: operations.QuestionIn, session: Session = Depends(get_session)
) -> operations.QuestionOut:
    return operations.store_question(session, question)


@router.get("/questions")
def get_random_questions(
    session: Session = Depends(get_session),
    questions_amount: int = 5,
    alternatives_amount: int = 4,
) -> list[operations.QuestionIn]:
    return operations.generate_random_questions(
        session,
        alternatives_amount=alternatives_amount,
        questions_amount=questions_amount,
    )


@router.post("/questions", status_code=201)
def post_questions(
    questions: list[operations.QuestionIn], session: Session = Depends(get_session)
) -> None:
    operations.store_questions(session, questions)
