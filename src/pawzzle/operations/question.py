import random

from sqlalchemy.orm import Session

from pawzzle.db.models import Question
from pawzzle.db import dog as db_dog
from pawzzle.db import question as db_question


def create_random_question(session: Session, *, alternatives_amount: int) -> Question:
    dogs = db_dog.get_all_dogs(session)
    correct_dog = random.choice(dogs)
    question = db_question.store_question(
        f"Which one is a {correct_dog.breed}",
        alternatives=random.sample(dogs, k=alternatives_amount),
        correct_dog=correct_dog,
        session=session,
    )

    return question
