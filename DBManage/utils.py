from typing import Any
from configparser import ConfigParser
import requests


def format_companies(data: dict):
    """
    Форматирует данные компаний для записи в БД
    :param data: Входные данные
    :return:
    """
    result = []
    for company_name, company_key in data.items():
        url = f"https://api.hh.ru/employers/{company_key}"
        company_info = requests.get(url).json()
        temp_dict = {"company_id": company_key, "company_name": company_name,
                     "company_url": company_info['alternate_url'], "description": company_info['description']}
        result.append(temp_dict)
    return result


def format_vacancy(data: list[dict[str, Any]]):
    """
    Форматируют данные с вакансиями для записи в БД
    :param data: Вакансии
    :return: список форматированных вакансий
    """
    result = []
    for vacancy in data:
        temp_dict = {"vacancy_id": vacancy['id'], "company_id": vacancy['employer']['id'],
                     "salary": vacancy['salary'], "vacancy_url": vacancy['url'],
                     "description": vacancy['snippet']['requirement']}
        result.append(temp_dict)
    return result


def config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception()

    return db
