from models import Vacancy, Skill, ConnectionTable

from sqlalchemy.orm import Session

from schemas import VacancySchema, VacancySchemaId, VacancySchemaIdSkills, VacancySchemaSkills

from sqlalchemy import Table, select, and_
import logging

logging.basicConfig(level=logging.INFO, filename='data_logging.log',
                    format='%(levelname)s (%(asctime)s: %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %I:%M:%S',
                    filemode='w',
                    encoding='utf-8')

logging.info('crud started')

class Crud:
    @classmethod
    def get_vacancy(cls, db: Session, skip: int = 0, limit: int = 100) -> list[VacancySchemaId]:

        vacancies_models = db.query(Vacancy).offset(skip).limit(limit).all()
        logging.info('Данные были взяты успешно')
        try:
            vacancies = [VacancySchemaId.model_validate(vac) for vac in vacancies_models]
            logging.info('Данные были преобразованы успешно')
            return vacancies
        except Exception as ex:
            logging.info(f'Ошибка при преобразовании данных из БД: {ex}')

    @classmethod
    def get_skill(cls, db: Session, skip: int = 0, limit: int = 100) -> VacancySchema:
        vacancy_model = db.query(Skill).offset(skip).limit(limit).first()
        vacancy = VacancySchema.from_orm(vacancy_model)
        return vacancy

    @classmethod
    def get_ct(cls, db: Session, skip: int = 0, limit: int = 100):
        return db.query(ConnectionTable).offset(skip).limit(limit).all()

    @classmethod
    def get_skills_for_vacancy(cls, db: Session, id_vacancy: int):
        try:
            skills = db.query(Skill).join(ConnectionTable, Skill.id == ConnectionTable.c.skill_id).filter(
                ConnectionTable.c.vacancy_id == id_vacancy).all()
            skill_names = [skill.name for skill in skills]
        except Exception as ex:
            logging.error(ex)
        return skill_names

    @classmethod
    def get_vacancy_by_id(cls, db: Session, vacancy_id: int):
        logging.info('get vacancy by id')
        return db.query(Vacancy).filter(Vacancy.id == vacancy_id).first()

    @classmethod
    def get_skill_by_id(cls, db: Session, skill_id: int):
        return db.query(Skill).filter(Skill.id == skill_id).first()

    @classmethod
    def create_vacancy_scheme(cls, db: Session, vacancy: VacancySchemaSkills):
        try:
            _vacancy = Vacancy(name=vacancy.name,
                               salary=vacancy.salary, text=vacancy.text,
                               created=vacancy.created)
            db.add(_vacancy)
            db.commit()
            db.refresh(_vacancy)
            _vacancy = VacancySchemaIdSkills.from_orm(_vacancy)
            skills = cls.get_skills_for_vacancy(db=db, id_vacancy=_vacancy.id)
            _vacancy.skills = skills
        except Exception as ex:
            logging.error(ex)
        return _vacancy

    @classmethod
    def create_vacancy(cls, db: Session, name: str, salary: int, text: str, created: str):
        _vacancy = Vacancy(name=name, salary=salary, text=text, created=created)
        db.add(_vacancy)
        db.commit()
        db.refresh(_vacancy)
        return _vacancy

    @classmethod
    def create_skill(cls, db: Session, name: str):
        _skill = Skill(name=name)
        db.add(_skill)
        db.commit()
        db.refresh(_skill)
        return _skill

    @classmethod
    def create_ct(cls, db: Session, vacancy_id: int, skill_id: int):
        connection_row = ConnectionTable.insert().values(vacancy_id=int(vacancy_id), skill_id=int(skill_id))
        db.execute(connection_row)
        db.commit()

    @classmethod
    def remove_vacancy(cls, db: Session, vacancy_id: int):
        try:
            _vacancy = cls.get_vacancy_by_id(db=db, vacancy_id=vacancy_id)
            vacancy_schema = VacancySchemaIdSkills.from_orm(_vacancy)
            skills = cls.get_skills_for_vacancy(db=db, id_vacancy=vacancy_id)
            vacancy_schema.skills = skills

            db.query(ConnectionTable).filter(ConnectionTable.c.vacancy_id == vacancy_id).delete(
                synchronize_session='fetch')

            db.query(Vacancy).filter(Vacancy.id == vacancy_id).delete(synchronize_session='fetch')

            db.commit()
        except Exception as ex:
            logging.error(ex)
        return vacancy_schema

    @classmethod
    def remove_skill(cls, db: Session, skill_id: int):
        _skill = cls.get_skill_by_id(db=db, skill_id=skill_id)
        db.delete(_skill)
        db.commit()

    @classmethod
    def update_vacancy(cls, db: Session, vacancy_id: int, vacancy: VacancySchemaSkills):
        _vacancy = cls.get_vacancy_by_id(db=db, vacancy_id=vacancy_id)
        _vacancy.name = vacancy.name
        _vacancy.salary = vacancy.salary
        _vacancy.text = vacancy.text
        _vacancy.created = vacancy.created

        db.commit()
        db.refresh(_vacancy)
        _vacancy = VacancySchemaIdSkills.from_orm(_vacancy)
        _vacancy.skills = vacancy.skills
        return _vacancy

    @classmethod
    def update_skill(cls, db: Session, skill_id: int, name: str):
        _skill = cls.get_skill_by_id(db=db, skill_id=skill_id)
        _skill.name = name
        db.commit()
        db.refresh(_skill)
        return _skill

    @classmethod
    def get_vacancies_by_skills(cls, db: Session, skill_names: list):
        try:
            subquery = db.query(ConnectionTable.c.vacancy_id).join(Skill).filter(Skill.name.in_(skill_names)).group_by(
                ConnectionTable.c.vacancy_id).having(
                and_(*(db.query(Skill).filter(Skill.name == skill_name).count() > 0 for skill_name in skill_names))
            ).subquery()

            vacancies = db.query(Vacancy).filter(Vacancy.id.in_(subquery)).all()

            result = []
            for vacancy in vacancies:
                logging.info(type(vacancy))
                _vacancy = VacancySchemaIdSkills.from_orm(vacancy)
                skills = [skill.name for skill in db.query(Skill).join(ConnectionTable).filter(
                    ConnectionTable.c.vacancy_id == vacancy.id).all()]
                _vacancy.skills = skills
                result.append(_vacancy)
            return result
        except Exception as e:
            logging.error(f'Error fetching vacancies by skills: {e}')
            return []
