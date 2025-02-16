
from typing import List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict
import logging


logging.basicConfig(level=logging.INFO, filename='data_logging.log',
                    format='%(levelname)s (%(asctime)s: %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %I:%M:%S',
                    filemode='w',
                    encoding='utf-8')

logging.info("schemas")


class VacancySchema(BaseModel):
    name: str
    salary: str
    text: Union[str, None] = None

    created: Union[str, None] = None

    # class Config:
    #     orm_mode = True
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)

class VacancySchemaId(VacancySchema):
    id: int


class VacancySchemaSkills(VacancySchema):
    skills: Union[list[str], None] = None


class VacancySchemaIdSkills(VacancySchemaId, VacancySchemaSkills):
    pass
