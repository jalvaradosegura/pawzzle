from pydantic import BaseModel


class DogIn(BaseModel):
    id: int
    breed: str
    info_url: str | None
    img_name: str | None


class DogOut(DogIn):
    pass


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


class AnswersIn(BaseModel):
    answers: list[AnswerIn]


class Quiz(BaseModel):
    target_date: str


class QuizIn(Quiz):
    questions: list[QuestionIn]
    target_date: str = ""


class QuizOut(Quiz):
    id: int
    questions: list[QuestionOut]
