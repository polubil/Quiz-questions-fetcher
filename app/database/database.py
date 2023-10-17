from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import get_key

# получаем данные для подключения к БД из .env файла, который находится в корне проекта.
db_user = get_key('.env', 'POSTGRES_USER')
db_pw = get_key('.env', 'POSTGRES_PASSWORD')
db_name = get_key('.env', 'POSTGRES_DB')

db_url = f'postgresql://{db_user}:{db_pw}@db:5432/{db_name}'

engine = create_engine(url=db_url)

SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()
