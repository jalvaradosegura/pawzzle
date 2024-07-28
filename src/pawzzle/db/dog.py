from sqlalchemy import func
from sqlalchemy.orm import Session

from pawzzle.db.models import Dog


def get_all_dogs(
    session: Session, limit: None | int = None, offset: None | int = None
) -> list[Dog]:
    query = session.query(Dog)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)

    return query.all()


def get_dog(id: int, session: Session) -> Dog:
    return session.get_one(Dog, id)


def store_dog(breed: str, session: Session) -> Dog:
    dog = Dog(breed=breed)
    session.add(dog)
    session.commit()
    return dog


def randomly_get_n_dogs(n: int, session: Session) -> list[Dog]:
    query = session.query(Dog)
    return query.order_by(func.random()).limit(n).all()
