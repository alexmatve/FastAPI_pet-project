import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

import numpy as np

import logging


# Парсинг сайта rabota.ru

def parser(URL_TEMPLATE):
    r = requests.get(URL_TEMPLATE)
    src = r.text

    soup = bs(src, "html.parser")
    items = soup.find_all('article',
                          {"class": "vacancy-preview-card vacancy-preview-card_promoted vacancy-preview-card_snippet"})

    data = {"id": [], "name": [], "salary": [], "text": [], "created": [], "skills": [], "links": []}

    i = 1
    for item in items:
        info = item.find("a", {"class": "vacancy-preview-card__title_border"})
        title = info.text.strip()
        salary = item.find("div", {"class": "vacancy-preview-card__salary"}).text.strip()
        description = item.find("div", {"class": "vacancy-preview-card__short-description"}).text.strip()
        created = None
        link = "https://www.rabota.ru" + info.get("href")
        data['id'].append(i)
        data['name'].append(title)
        data['salary'].append(salary)
        data['text'].append(description)
        data['created'].append(None)
        data["links"].append(link)
        i += 1

    for link in data["links"]:
        skills = []
        URL_TEMPLATE = link
        r = requests.get(URL_TEMPLATE)
        src = r.text
        soup = bs(src, "html.parser")
        items = soup.find_all('article', {"class": "vacancy-card"})
        for item in items:
            all_skills = item.find_all("div", {"class": "vacancy-card__skills-item"})
            for s in all_skills:
                skills.append(s.text.strip())
        data["skills"].append(skills)
    return data


logging.basicConfig(level=logging.INFO, filename='parsing_logging.log',
                    format='%(levelname)s (%(asctime)s: %(message)s (Line: %(lineno)d) [%(filename)s]',
                    datefmt='%d/%m/%Y %I:%M:%S',
                    filemode='w',
                    encoding='utf-8')

logging.info('Парсинг сайта rabota.ru')
data = parser(URL_TEMPLATE="https://www.rabota.ru/vacancy")

logging.info('Начало работы с DataFrame для извлечения Skills и ConnectionTable')
df = pd.DataFrame(data)

df_expanded = df.explode('skills')
df_connection = pd.DataFrame({'id': df_expanded['id'], 'skill': df_expanded['skills']})

all_skills = []
for group in data['skills']:
    for s in group:
        all_skills.append(s)
set_skills = set(all_skills)

df_skills = pd.DataFrame({"skill": list(set_skills), "skill_id": np.arange(1, len(set_skills) + 1)})

df_merged = df_connection.merge(df_skills, on='skill', how='left')

df_merged.dropna(inplace=True)

df_merged['skill_id'] = df_merged['skill_id'].astype(int)

df_merged.drop(columns='skill', inplace=True)

df_merged.reset_index(drop=True, inplace=True)

df_skills.rename(columns={'skill_id': 'id', 'skill': 'name'}, inplace=True)

df_skills = df_skills[['id', 'name']]
print(df_skills.head())
print("---------------------------")
print(df.head())
print("---------------------------")

print(df_merged.head())
