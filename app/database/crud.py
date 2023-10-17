from typing import List, Type

from sqlalchemy.orm import Session
from app.database import models, schemas


def get_question(db: Session, id: int) -> models.Question | None:
    """
    Получить вопрос по его идентификатору.
    :param db: сессия базы данных
    :param id: идентификатор к получению
    :return: вопрос
    """
    return db.query(models.Question).filter(models.Question.id == id).first()


def get_questions(db: Session, n: int = 1) -> list[Type[models.Question]]:
    """
    Получить список из n случайных вопросов.
    :param db: сессия базы данных
    :param n: максимальное количество возвращаемых вопросов
    :return: список из n вопросов
    """
    return db.query(models.Question).limit(n).all()


def get_questions_amount(db: Session) -> int:
    """
    Получить общее количество вопросов
    """
    return db.query(models.Question).count()


def add_questions(db: Session, questions: List[schemas.Question]) -> models.Question:
    """
    Добавить вопросы в базу данных.
    :param db: сессия базы данных
    :param questions: список вопросов, которые нужно добавить в базу данных.
    :return: последний добавленный вопрос
    """
    db.add_all(questions)
    db.commit()
    return questions[-1]


def get_question_ids(db: Session) -> list[int]:
    """Получить список из id вопросов, имеющихся в базе данных"""
    return [item.id for item in db.query(models.Question)]
