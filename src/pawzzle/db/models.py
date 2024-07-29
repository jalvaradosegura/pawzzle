from typing import Any

from sqlalchemy import Column, ForeignKey, String, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


question_dog_association = Table(
    "question_dog_association",
    Base.metadata,
    Column("question_id", ForeignKey("question.id"), primary_key=True),  # type: ignore
    Column("dog_id", ForeignKey("dog.id"), primary_key=True),  # type: ignore
)

quiz_question_association = Table(
    "quiz_question_association",
    Base.metadata,
    Column("quiz_id", ForeignKey("quiz.id"), primary_key=True),  # type: ignore
    Column("question_id", ForeignKey("question.id"), primary_key=True),  # type: ignore
)


class Dog(Base):
    __tablename__ = "dog"
    id: Mapped[int] = mapped_column(primary_key=True)
    breed: Mapped[str] = mapped_column(String(30))

    questions_where_correct: Mapped[list["Question"]] = relationship()

    questions_as_alternative: Mapped[list["Question"]] = relationship(
        secondary=question_dog_association, back_populates="alternatives"
    )

    def to_dict(self) -> dict[str, Any]:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }


class Question(Base):
    __tablename__ = "question"
    id: Mapped[int] = mapped_column(primary_key=True)
    text: Mapped[str] = mapped_column(String(50))

    correct_dog_id: Mapped[int] = mapped_column(ForeignKey("dog.id"))
    correct_dog: Mapped["Dog"] = relationship(back_populates="questions_where_correct")

    alternatives: Mapped[list["Dog"]] = relationship(
        secondary=question_dog_association, back_populates="questions_as_alternative"
    )

    quizzes: Mapped[list["Quiz"]] = relationship(
        secondary=quiz_question_association, back_populates="questions_as_alternative"
    )


class Quiz(Base):
    __tablename__ = "quiz"
    id: Mapped[int] = mapped_column(primary_key=True)

    questions_as_alternative: Mapped[list["Question"]] = relationship(
        secondary=quiz_question_association, back_populates="quizzes"
    )
