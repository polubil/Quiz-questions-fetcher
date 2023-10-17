from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_fetching_questions():
    start_amount = client.get("/").json()["total questions"]
    client.post("/add_questions", json={"questions_num": 100})
    end_amount = client.get("/").json()["total questions"]
    assert start_amount == end_amount - 100


def test_question_getting():
    response = client.get("/question", params={'id': -1})
    assert response.status_code == 404
    question_id = client.post("/add_questions", json={"questions_num": 1}).json().get("id")
    response = client.get("/question", params={'id': question_id})
    assert response.json().get('id') == question_id


def test_question_getting_multiple():
    response = client.get("/questions", params={'n': 5})
    assert len(response.json()) == 5
