from typing import Any

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Table, func
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
    breed: Mapped[str] = mapped_column(String(100))
    image_url: Mapped[str | None] = mapped_column(String(350), nullable=True)
    info_url: Mapped[str | None] = mapped_column(String(350), nullable=True)

    questions_where_correct: Mapped[list["Question"]] = relationship()

    questions_as_alternative: Mapped[list["Question"]] = relationship(
        secondary=question_dog_association, back_populates="alternatives"
    )

    answers: Mapped[list["Answer"]] = relationship()

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
        secondary=quiz_question_association, back_populates="questions"
    )

    answers: Mapped[list["Answer"]] = relationship()

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "correct_dog": self.correct_dog.to_dict(),
            "alternatives": [a.to_dict() for a in self.alternatives],
        }


class Quiz(Base):
    __tablename__ = "quiz"
    id: Mapped[int] = mapped_column(primary_key=True)

    questions: Mapped[list["Question"]] = relationship(
        secondary=quiz_question_association, back_populates="quizzes"
    )


class Answer(Base):
    __tablename__ = "answer"
    id: Mapped[int] = mapped_column(primary_key=True)
    correct: Mapped[Boolean] = mapped_column(Boolean)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    question_id: Mapped[int] = mapped_column(ForeignKey("question.id"))
    question: Mapped[Question] = relationship(back_populates="answers")

    dog_id: Mapped[int] = mapped_column(ForeignKey("dog.id"))
    dog: Mapped[Dog] = relationship(back_populates="answers")

    def to_dict(self) -> dict[str, Any]:
        return {
            column.name: getattr(self, column.name) for column in self.__table__.columns
        }
