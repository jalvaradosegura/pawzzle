from fastapi import APIRouter, Depends
from fastapi_pagination import Page
from fastapi_pagination.ext.sqlalchemy import paginate  # type: ignore
from sqlalchemy import select
from sqlalchemy.orm import Session

from pawzzle.dependencies import get_session
from pawzzle.db.models import Dog
from pawzzle.operations.schemas import DogOut, RarenessUpdate
from pawzzle.operations.rareness import update_rareness

router = APIRouter()


@router.get("/dogs")
def get_dogs(session: Session = Depends(get_session)) -> Page[DogOut]:
    return paginate(session, select(Dog))


@router.put("/dogs")
def put_dogs(
    rareness_update_list: list[RarenessUpdate], session: Session = Depends(get_session)
):
    return update_rareness(session, rareness_update_list)
