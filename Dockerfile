FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade --no-cache-dir -r /app/requirements.txt
COPY .env /app/.env
COPY test_main.py /app/test_main.py
COPY app /app/app
CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0"]