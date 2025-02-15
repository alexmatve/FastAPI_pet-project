import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_get_vacancy_by_id():
    response = client.get('/vacancy/1')
    assert response.status_code == 200
    data = response.json()
    assert data['name'] == "Продавец (м. Раменки)"
    assert data['salary'].replace('\xa0', ' ') == "от 67 000 руб."
    assert data['text'] == "Красное & Белое» - розничная сеть магазинов формата «У ДОМА». Много лет мы радуем нашего покупателя приятными ценами, удобным расположением и качественными продуктами. Мы присутствуем в каждом уголке России. Сейчас в Компании работает более 125 000 классных сотрудников и нам не хватает именно тебя…"
    assert data['skills'] == ['ответственность', 'пунктуальность', 'стрессоустойчивость',
                              'грамотная речь', 'обучаемость', 'доброжелательность', 'прием товар', 'Грамотная речь',
                              'Стрессоустойчивость', 'Ответственность', 'Обучаемость', 'Доброжелательность',
                              'Пунктуальность']
    assert data['id'] == 1


def test_post_vacancy():
    response = client.post('/vacancy/', params={"name": "Teacher",
                                              "salary": "40000",
                                              "text": "Biology",
                                              "created": '05.05.24'})
    assert response.status_code == 200

    data = response.json()
    assert data['name'] == "Teacher"
    assert data['salary'].replace('\xa0', ' ') == "40000"
    assert data['text'] == "Biology"
    assert data['skills'] == []
    assert data['created'] == '05.05.24'


#
def test_delete_vacancy():
    response = client.delete('/vacancy/30')
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == 30


def test_put_vacancy():
    response = client.put('/vacancy/10', params={"name": "Doctor",
                                               "salary": "50000",
                                               "text": "Dental",
                                               "created": "07.02.24"})
    assert response.status_code == 200

    data = response.json()

    assert data['name'] == 'Doctor'
    assert data['salary'] == '50000'
    assert data['text'] == 'Dental'
    assert data['created'] == '07.02.24'
    assert data['id'] == 10


def test_get_vacancy_skill():
    response = client.get('/vacancy/skill/', params={'skills': ["MS Office  Excel"]})
    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert data[0]['name'] == 'Оператор колл-центра на входящую линию (удаленно)'
    assert data[0]['salary'].replace('\xa0', ' ') == '20 000 — 30 000 руб.'
    assert data[0]['id'] == 16


def test_get_vacancies():
    response = client.get('/vacancy/')
    assert response.status_code == 200

    data = response.json()
    assert len(data) == 5;
    assert data[0]['id'] == 1
    assert data[-1]['id'] == 5
