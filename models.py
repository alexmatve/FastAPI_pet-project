
from sqlalchemy.orm import relationship, sessionmaker, Mapped
import sqlalchemy

import os

from sqlalchemy import Table, Column, Integer, String, MetaData, \
    create_engine, ForeignKey
from dotenv import load_dotenv

import logging


logging.basicConfig(level=logging.INFO, filename='data_logging.log',
                    format='%(levelname)s (%(asctime)s: %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %I:%M:%S',
                    filemode='w',
                    encoding='utf-8')

logging.info("models")


load_dotenv()

Base = sqlalchemy.orm.declarative_base()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

Session = sessionmaker(autoflush=True, bind=engine)
session = Session()

ConnectionTable = Table('connectiontable', Base.metadata,
                        Column('vacancy_id', Integer, ForeignKey("vacancy.id", )),
                        Column('skill_id', Integer, ForeignKey("skill.id")))


class Vacancy(Base):
    __tablename__ = 'vacancy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    salary = Column(String)
    text = Column(String, nullable=True)
    created = Column(String, nullable=True)

    skills_t = relationship('Skill', secondary=ConnectionTable, back_populates='vacancies', cascade='all, delete')


class Skill(Base):
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True, unique=True, autoincrement=True)
    name = Column(String)

    vacancies = relationship('Vacancy', secondary=ConnectionTable, back_populates='skills_t', cascade='all, delete')


#Base.metadata.create_all(engine)

#
# session.close()
# engine.dispose()

