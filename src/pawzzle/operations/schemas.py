from pydantic import BaseModel


class DogSchema(BaseModel):
    id: int
    breed: str


class QuestionSchema(BaseModel):
    text: str
    correct_dog: DogSchema
    alternatives: list[DogSchema]
