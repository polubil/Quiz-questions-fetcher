# Quiz-questions-fetcher

Сервис позволяет собирать, хранить и предоставлять вопросы для викторин, полученные из открытого источника -  jService API.

# Installation

1. Скопируйте Git-репозиторий и перейдите в директорию проекта:

   ```
   git clone polubil/Quiz-questions-fetcher
   cd Quiz-questions-fetcher
   ```

2. При необходимости, измените файл .env_example и введите Ваши данные, которые будут использоваться базой данных:

    ```
    POSTGRES_USER = имя пользователя
    POSTGRES_PASSWORD = пароль пользователя 
    POSTGRES_DB = название базы данных.
    ```

    Переименуйте файл ".env_example" в ".env"

3. Соберите и запустите Docker-контейнер.

   ```
   docker-compose build
   docker-compose up
   ```

# Usage

1. После первого запуска в сервисе нет сохраненных вопросов, в чем можно убедиться, отправив get-запрос на '/'. В качестве ответа будет предоставлено общее количество сохраненных вопросов. Добавьте несколько вопросов, послав post-запрос на адрес /add_questions с телом:

   ```
   {questions_num: 100} # количество может быть любым неотрицательным числом.
   ```
   В качестве ответа на запрос будет возвращен последний добавленный в БД вопрос.
   
2. С помощью get-запроса на /question?id=some_id можно получить вопрос с определенным идентификатором (id должен соответствовать id в jService)
3. С помощью get-запроса на /questions?n=amount можно получить заданное количество вопросов.

# Testing

1. Тесты можно запустить из корневой директории проекта командой:

   ```
   pytest test_main.py
   ```
