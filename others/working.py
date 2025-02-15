from datetime import datetime
from enum import Enum
from typing import List, Optional, Union
from pydantic import BaseModel, Field

from fastapi import FastAPI, Request, status
from fastapi.encoders import jsonable_encoder
import fastapi.exceptions
from fastapi.responses import JSONResponse

vacancies = [
    {"id": 1, "name": "admin", "salary": 1000, "text": "Maintain", "skills": ['strength', 'kindness']},
    {"id": 2, "name": "investor", "salary": 2000, "text": "jump", "skills": ['length', 'respect']},
    {"id": 3, "name": "trader", "salary": 3000, "text": "hop", "skills": ['short', 'knowledge']},
    {"id": 4, "name": "investor", "salary": 4000, "text": "think", "skills": ['smart', 'small']}
]


# uvicorn schemas:app --reload

class Vacancy(BaseModel):
    id: int
    name: str
    salary: int
    text: Union[str, None] = None
    skills: Union[List[str], None] = None


app = FastAPI()


@app.get('/vacancy/', response_model=List[Vacancy])
def get_vacancy():
    return vacancies


@app.get('/vacancy/{id_vacancy}')
def get_id_vacancy(id_vacancy: int):
    ans_vacancy = [vacancy for vacancy in vacancies if vacancy.get('id') == id_vacancy][0].copy()
    ans_vacancy['created'] = str("sometime")
    return ans_vacancy


@app.post('/vacancy/')
def add_vacancy(vacancy: List[Vacancy]):
    vacancies.extend(vacancy)
    # ans_vacancy = vacancies[-1]
    # ans_vacancy.update({"created": str(datetime.now())})
    ans_vacancy = vacancies[-1].copy()
    # ans_vacancy['created'] = str("sometime")
    return {'created': 'today', "data": ans_vacancy}


@app.delete('/vacancy/{id_vacancy}')
def delete_id_vacancy(id_vacancy: int):
    for vacancy in vacancies:
        if vacancy.get('id') == id_vacancy:
            ans_vacancy = vacancy.copy()
            vacancies.remove(vacancy)
    return ans_vacancy


@app.put('/vacancy/{id_vacancy}')
def put_id_vacancy(id_vacancy: int, vacancy: Vacancy):
    for i in range(len(vacancies)):
        if vacancies[i].get('id') == id_vacancy:
            update_vacancy = jsonable_encoder(vacancy)
            vacancies[i] = update_vacancy
    return vacancy
