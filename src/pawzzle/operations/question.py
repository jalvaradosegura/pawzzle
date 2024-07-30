import random

from sqlalchemy.orm import Session

from pawzzle.db import dog as db_dog
from pawzzle.operations.schemas import DogSchema, QuestionSchema


def generate_random_question(
    session: Session, *, alternatives_amount: int
) -> QuestionSchema:
    alternatives = db_dog.randomly_select_n_dogs(alternatives_amount, session)
    correct_dog = random.choice(alternatives)

    question = QuestionSchema(
        text=f"Which one is a {correct_dog.breed}",
        correct_dog=DogSchema(**correct_dog.to_dict()),
        alternatives=[DogSchema(**dog.to_dict()) for dog in alternatives],
    )

    return question
