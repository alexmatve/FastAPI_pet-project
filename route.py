
from typing import List, Optional, Union

from fastapi import FastAPI, Request, status, APIRouter, Depends, Query


from schemas import VacancySchema, VacancySchemaId, VacancySchemaIdSkills, VacancySchemaSkills
from crud import Crud
# from test import session
from models import session
import logging
logging.basicConfig(level=logging.INFO, filename='data_logging.log',
                    format='%(levelname)s (%(asctime)s: %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %I:%M:%S',
                    filemode='w',
                    encoding='utf-8')
router = APIRouter(prefix='/vacancy', tags=["Вакансии"])


@router.get('/')
def get_vacancy() -> list[VacancySchemaId]:
    logging.info('Метод get вызвался')
    vacancies = Crud.get_vacancy(db=session, skip=0, limit=5)
    logging.info('Обращение к ORM прошло')
    return vacancies


@router.get('/{id_vacancy}')
def get_id_vacancy(id_vacancy: int) -> VacancySchemaIdSkills:
    vacancy = Crud.get_vacancy_by_id(db=session, vacancy_id=id_vacancy)
    vacancy = VacancySchemaIdSkills.from_orm(vacancy)

    skills = Crud.get_skills_for_vacancy(db=session, id_vacancy=id_vacancy)
    vacancy.skills = skills
    return vacancy


@router.post('/')
def add_vacancy(vacancy: VacancySchemaSkills = Depends()) -> VacancySchemaIdSkills:
    new_vacancy = Crud.create_vacancy_scheme(db=session, vacancy=vacancy)
    return new_vacancy


@router.delete('/{id_vacancy}')
def delete_vacancy(id_vacancy: int) -> VacancySchemaIdSkills:
    vacancy = Crud.remove_vacancy(db=session, vacancy_id=id_vacancy)
    return vacancy


@router.put('/{id_vacancy}')
def put_vacancy(id_vacancy: int, vacancy: VacancySchemaSkills = Depends()) -> VacancySchemaIdSkills:
    new_vacancy = Crud.update_vacancy(db=session, vacancy_id=id_vacancy, vacancy=vacancy)
    return new_vacancy


@router.get("/skill/")
def read_vacancies_by_skills(skills: List[str] = Query(...)):
    vacancies = Crud.get_vacancies_by_skills(db=session, skill_names=skills)
    return vacancies
