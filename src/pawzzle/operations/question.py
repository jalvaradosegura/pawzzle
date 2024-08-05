import random

from sqlalchemy.orm import Session

from pawzzle.db.dog import select_all_dogs, randomly_select_n_dogs
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


def generate_random_questions(
    session: Session, *, alternatives_amount: int, questions_amount: int
) -> list[QuestionIn]:
    return [
        generate_random_question(session, alternatives_amount=alternatives_amount)
        for _ in range(questions_amount)
    ]


def store_question(session: Session, question: QuestionIn) -> QuestionOut:
    all_dogs_id = {alternative.id for alternative in question.alternatives}
    all_dogs_id.add(question.correct_dog.id)
    dogs = select_all_dogs(session, filter_=all_dogs_id)
    dogs_map = {dog.id: dog for dog in dogs}

    stored_question = insert_question(
        session,
        text=question.text,
        alternatives=[
            dogs_map[alternative.id] for alternative in question.alternatives
        ],
        correct_dog=dogs_map[question.correct_dog.id],
    )
    question_with_id = QuestionOut(id=stored_question.id, **question.model_dump())

    return question_with_id
