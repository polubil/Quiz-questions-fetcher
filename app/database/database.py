from time import sleep

from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import get_key

# получаем данные для подключения к БД из .env файла, который находится в корне проекта.
db_user = get_key('.env', 'POSTGRES_USER')
db_pw = get_key('.env', 'POSTGRES_PASSWORD')
db_name = get_key('.env', 'POSTGRES_DB')

db_url = f'postgresql://{db_user}:{db_pw}@db:5432/{db_name}'

max_retries, retries = 10, 0
while 1:
    try:
        engine = create_engine(url=db_url)
        break
    except OperationalError as e:
        retries += 1
        if max_retries <= retries:
            raise e
        print(f"База данных недоступна... Повторная попытка подключения через 10 секунд ({retries})...")
        sleep(10)


SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
