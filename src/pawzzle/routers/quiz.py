from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from pawzzle import operations
from pawzzle.cache.types import Cache
from pawzzle.dependencies import get_session, get_cache

router = APIRouter()


@router.post("/quiz", status_code=201)
def post_quiz(
    quiz_in: operations.QuizIn,
    session: Session = Depends(get_session),
):
    return operations.store_quiz(session, quiz_in)


@router.post("/quizzes", status_code=201)
def post_quizzes(
    quizzes_in: list[operations.QuizIn],
    session: Session = Depends(get_session),
):
    for quiz_in in quizzes_in:
        operations.store_quiz(session, quiz_in)


@router.get("/quiz/random")
def get_quiz_random(session: Session = Depends(get_session)) -> operations.QuizIn:
    return operations.generate_random_quiz(session, questions_amount=10, target_date="")


@router.get("/quiz/{quiz_id}")
def get_quiz(
    quiz_id: int, session: Session = Depends(get_session)
) -> operations.QuizOut:
    return operations.get_quiz(session, quiz_id)


@router.get("/quiz")
def get_todays_quiz(
    cache: Cache = Depends(get_cache), session: Session = Depends(get_session)
) -> operations.QuizOut:
    return operations.get_todays_quiz(cache, session)
