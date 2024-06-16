from typing import Any

import requests

from APImanger.HeadHunterAPI import HeadHunterAPI


def format_companies(data: dict):
    result = [{}]
    for company_name, company_key in data.items():
        url = f"https://api.hh.ru/employers/{company_key}"
        company_info = requests.get(url).json()
        temp_dict = {"company_id": company_key, "company_name": company_name,
                     "company_url": company_info['alternate_url'], "description": company_info['description']}
        result.append(temp_dict)
    return result


def format_vacancy(data: list[dict[str, Any]]):
    result = [{}]
    for vacancy in data:
        temp_dict = {"vacancy_id": vacancy['id'], "company_id": vacancy['employer']['id'],
                     "salary": vacancy['salary'], "vacancy_url": vacancy['url'],
                     "description": vacancy['snippet']['requirement']}
        result.append(temp_dict)
    return result
