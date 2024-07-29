from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from pawzzle.db.init import init_db
from pawzzle.operations import question as operations
from pawzzle.operations.schemas import QuestionSchema

router = APIRouter()


def get_session():  # pragma: no cover
    engine, _ = init_db(
        "sqlite:///:memory:",
        echo=False,  # type: ignore
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # type: ignore
    )
    with Session(engine) as session:
        yield session


@router.get("/question")
def get_random_question(
    session: Session = Depends(get_session), alternatives_amount: int = 4
) -> QuestionSchema:
    return operations.generate_random_question(
        session, alternatives_amount=alternatives_amount
    )
