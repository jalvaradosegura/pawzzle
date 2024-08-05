from typing import Any, TypedDict

from sqlalchemy import func, insert
from sqlalchemy.orm import Session

from pawzzle.db.models import Dog


def select_all_dogs(
    session: Session,
    *,
    limit: None | int = None,
    offset: None | int = None,
    filter_: list[int] | set[int] | None = None,
) -> list[Dog]:
    query = session.query(Dog)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    if filter_:
        query = query.where(Dog.id.in_(filter_))

    return query.all()


def select_dog(session: Session, id: int) -> Dog:
    return session.get_one(Dog, id)


def insert_dog(session: Session, breed: str, **extra_columns: dict[str, Any]) -> Dog:
    dog = Dog(breed=breed, **extra_columns)
    session.add(dog)
    session.commit()
    session.refresh(dog)
    return dog


def randomly_select_n_dogs(session: Session, n: int) -> list[Dog]:
    query = session.query(Dog)
    return query.order_by(func.random()).limit(n).all()


class BulkDogData(TypedDict):
    breed: str
    image_url: str
    info_url: str


def bulk_insert_dogs(session: Session, dogs_data: list[BulkDogData]):
    session.execute(insert(Dog), dogs_data)
    session.commit()
