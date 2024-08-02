import random

from sqlalchemy.orm import Session

from pawzzle.db.dog import Dog, select_dog, randomly_select_n_dogs
from pawzzle.db.question import insert_question
from pawzzle.operations.schemas import (
    QuestionIn,
    DogIn,
    QuestionOut,
)


def generate_random_question(
    session: Session, *, alternatives_amount: int
) -> QuestionIn:
    alternatives = randomly_select_n_dogs(session, alternatives_amount)
    correct_dog = random.choice(alternatives)

    question = QuestionIn(
        text=f"Which one is a {correct_dog.breed}",
        correct_dog=DogIn(**correct_dog.to_dict()),
        alternatives=[DogIn(**dog.to_dict()) for dog in alternatives],
    )

    return question


def store_question(session: Session, question: QuestionIn) -> QuestionOut:
    alternatives: list[Dog] = []
    for alternative in question.alternatives:
        dog = select_dog(session, alternative.id)
        alternatives.append(dog)

    correct_dog = select_dog(session, question.correct_dog.id)

    stored_question = insert_question(
        session,
        text=question.text,
        alternatives=alternatives,
        correct_dog=correct_dog,
    )
    question_with_id = QuestionOut(id=stored_question.id, **question.model_dump())

    return question_with_id
