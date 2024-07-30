from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from pawzzle.db.dog import insert_dog
from pawzzle.operations.schemas import DogSchema, QuestionSchema


@patch("pawzzle.routers.question.operations.generate_random_question")
def test_get_random_question(
    mocked_generate_random_question: MagicMock, session: Session, client: TestClient
):
    dog_1 = insert_dog("Poodle", session)
    dog_2 = insert_dog("Pug", session)
    dog_3 = insert_dog("Husky", session)
    dog_4 = insert_dog("Corgi", session)
    insert_dog("Samoyed", session)
    alternatives = [dog_1, dog_2, dog_3, dog_4]
    mocked_question_schema = QuestionSchema(
        text="Which one is a Poodle",
        correct_dog=DogSchema(**dog_1.to_dict()),
        alternatives=[DogSchema(**dog.to_dict()) for dog in alternatives],
    )
    mocked_generate_random_question.return_value = mocked_question_schema

    response = client.get("/question")

    assert response.status_code == 200
    assert response.json() == {
        "text": "Which one is a Poodle",
        "correct_dog": dog_1.to_dict(),
        "alternatives": [dog.to_dict() for dog in alternatives],
    }
