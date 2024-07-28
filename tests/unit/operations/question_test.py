import random
from sqlalchemy.orm import Session

from pawzzle.db.dog import store_dog
from pawzzle.operations.question import create_random_question


def test_create_question(session: Session):
    store_dog("Poodle", session)
    store_dog("Pug", session)
    store_dog("Husky", session)
    store_dog("Corgi", session)
    store_dog("Samoyed", session)
    random.seed(1)

    question = create_random_question(session, alternatives_amount=3)

    assert len(question.alternatives) == 3
    assert question.text == "Which one is a Pug"
