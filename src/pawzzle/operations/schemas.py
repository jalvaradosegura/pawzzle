from pydantic import BaseModel


class DogSchema(BaseModel):
    id: int
    breed: str
    image_url: str | None
    info_url: str | None


class QuestionSchema(BaseModel):
    text: str
    correct_dog: DogSchema
    alternatives: list[DogSchema]
