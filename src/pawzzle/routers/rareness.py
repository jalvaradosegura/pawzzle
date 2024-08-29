from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate  # type: ignore
from sqlalchemy import select
from sqlalchemy.orm import Session

from pawzzle.dependencies import get_session
from pawzzle.db.models import Dog
from pawzzle.operations.schemas import DogOut

router = APIRouter()


@router.get("/dogs")
def get_dogs(session: Session = Depends(get_session)) -> Page[DogOut]:
    return paginate(session, select(Dog))
