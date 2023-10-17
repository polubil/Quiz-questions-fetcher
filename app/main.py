from datetime import datetime
from time import sleep
from typing import List, Annotated

from fastapi import FastAPI, Depends, Body, HTTPException
from pydantic import PositiveInt
from sqlalchemy.exc import OperationalError

from sqlalchemy.orm import Session
import httpx

from app.database import models, crud, database, schemas


max_retries, retries = 10, 0
while 1:
    try:
        models.Base.metadata.create_all(bind=database.engine)
        break
    except OperationalError as e:
        retries += 1
        if max_retries <= retries:
            raise e
        print(f"База данных недоступна... Повторная попытка подключения через 10 секунд ({retries})...")
        sleep(10)

app = FastAPI()


def get_db() -> Session | None:
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def fetch_questions(n: int) -> List[dict] | int:
    """
    Функция получения вопросов с публичного API.
    :param n: количество вопросов к получению
    :return: вопросы в формате JSON
    """
    async with httpx.AsyncClient() as client:
        response = await client.get(
            url="https://jservice.io/api/random",
            params={"count": n},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=response.status_code, detail=response.text)
        return response.json()


@app.get("/")
async def root(db: Session = Depends(get_db)) -> dict[str, int]:
    """
    Возвращает количество вопросов.
    :param db:
    :return:
    """
    return {"total questions": crud.get_questions_amount(db)}


@app.get("/questions", response_model=list[schemas.Question])
async def get_questions(n: int = 1, db=Depends(get_db)):
    """
    Возвращает n вопросов.
    :param n: количество вопросов к получению
    :param db: сессия базы данных
    :return: respose as list with dicts
    """
    return crud.get_questions(db, n)


@app.get(".", response_model=schemas.Question)
async def get_questions(id: int, db=Depends(get_db)):
    """
    Возврачает вопрос с определенным id.
    :param id: id вопроса.
    :param db: сессия базы данных
    :return: response as dict
    """
    question = crud.get_question(db, id)
    if not question:
        raise HTTPException(status_code=404, detail="Вопроса с таким id нет.")
    return crud.get_question(db, id)


@app.post("/add_questions", response_model=schemas.Question)
async def add_questions(questions_num: Annotated[PositiveInt, Body(embed=True)], db: Session = Depends(get_db)) -> dict:
    """
    "В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные
    запросы (!)до тех пор, пока не будет получен уникальный вопрос для викторины(!)." при большом количестве запросов
    может быть так, что большинство из них уже есть в базе, в результате мы будем получать слишком много
    дубликатов и, рано или поздно, если не ограничить максимальное количество попыток, может быть переполнение стека
    из-за большого количества рекурсивных вызовов функции. Но ограничение количества попыток противоречит ТЗ, поэтому
    оставляем так.
    :param questions_num: количество вопросов, которые необходимо получить.
    :param db: сессия базы данных.
    :return: response as dict
    """
    print("Запрос", questions_num, "вопросов.")
    already_added_ids = crud.get_question_ids(db)
    questions_json = await fetch_questions(questions_num)
    questions, cnt = [], 0
    for i in questions_json:
        if i['id'] in already_added_ids:
            cnt += 1
            continue
        questions.append(models.Question(
            id=i['id'],
            question=i['question'],
            answer=i['answer'],
            created_at=i['created_at'],
            collected=datetime.now(),
        ))
    result = crud.add_questions(db, questions)
    print("Было", cnt, "повторяющихся вопросов.")
    if cnt > 0:
        result = await add_questions(cnt, db)
    return result
