from sqlalchemy.orm import relationship, sessionmaker
import sqlalchemy

import os

from sqlalchemy import Table, Column, Integer, String, MetaData, \
    create_engine, ForeignKey
import logging
from dotenv import load_dotenv

from parsing import df, df_skills, df_merged
from crud import Crud

from models import Vacancy, Skill, ConnectionTable

import logging


logging.basicConfig(level=logging.INFO, filename='data_logging.log',
                    format='%(levelname)s (%(asctime)s: %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %I:%M:%S',
                    filemode='w',
                    encoding='utf-8')

logging.info("db_operations")

load_dotenv()
#
#
# logging.info('Подключение к базе данных')
Base = sqlalchemy.orm.declarative_base()

DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_NAME = os.getenv('DB_NAME')

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

Session = sessionmaker(autoflush=True, bind=engine)
session = Session()

for line in df.values:
    Crud.create_vacancy(db=session, name=line[1], salary=line[2], text=line[3], created=line[4])

for line in df_skills.values:
    Crud.create_skill(db=session, name=line[1])

for line in df_merged.values:
    Crud.create_ct(db=session, vacancy_id=line[0], skill_id=line[1])

session.close()
engine.dispose()
