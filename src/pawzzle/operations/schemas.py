from pydantic import BaseModel


class DogIn(BaseModel):
    id: int
    breed: str
    image_url: str | None
    info_url: str | None


class Question(BaseModel):
    text: str
    correct_dog: DogIn
    alternatives: list[DogIn]


class QuestionIn(Question):
    pass


class QuestionOut(Question):
    id: int | None = None


class Answer(BaseModel):
    dog_id: int
    question_id: int


class AnswerIn(Answer):
    pass


class AnswerOut(Answer):
    id: int
    correct: bool
