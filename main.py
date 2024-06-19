import json
import os
from pprint import pprint
from DBManage.DBManage import DBManage
from DBManage.utils import config


path = input(
        f"Для поиска вакансий введите путь до файла или название 'json' файла с словарём интересующих вакансий"
        f" ничего не вводите для поиска компаний по умолчанию")
os.path.abspath(path=path)
if len(path) == 0:
    with open('default.json') as file:
        data = json.load(file)
else:
    with open(path) as file:
        data = json.load(file)

DBName = input("Введите имя БД в которой будет храниться информация")

config_path = input("Введите название файла 'ini'")

if len(config_path) == 0:
    config_path = 'database.ini'

DataBase = DBManage()
DataBase.init_DB(dbname=DBName, params=config(filename=config_path))
DataBase.load_companies_data(data)
DataBase.load_vacancies_data(data)

while True:
    command = int(input("""Введите номер команды
    1) Получить количество вакансий у каждой компании
    2) Получить все вакансии
    3) Получить среднюю зп
    4) Поиск вакансий с зп выше среднего
    5) Поиск вакансий по ключевому слову
    6) Завершить работу"""))

    match command:
        case 1:
            print("Компании и количество вакансии\n")
            pprint(DataBase.get_companies_and_vacancies_count())
        case 2:
            print("Все вакансии\n")
            pprint(DataBase.get_all_vacancies())
        case 3:
            print("Средняя зарплата\n")
            pprint(DataBase.get_avg_salary())
        case 4:
            print("Вакансии с ЗП выше среднего\n")
            pprint(DataBase.get_vacancies_with_higher_salary())
        case 5:
            print("Вакансии с ключевым словом в названии\n")
            keyword = input("Введите слово которое должно быть в названии")
            pprint(DataBase.get_vacancies_with_keyword(keyword))
        case 6:
            print("Останавливаю работу...")
            break
        case _:
            print("НЕ ВЕРНАЯ КОМАНДА!")
