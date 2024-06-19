import psycopg2
from DBManage.utils import format_companies
from APImanger.HeadHunterAPI import HeadHunterAPI


class DBManage:

    def __init__(self):
        self.conn = None
        self.cur = None
        pass

    def init_DB(self, dbname: str, params: dict) -> None:
        """
            Создаёт необходимые таблицы и базу данных с указанным именем и подключается к ней
            :param dbname:
            :param params:
        """
        conn = psycopg2.connect(dbname='postgres', **params)
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute(f'DROP DATABASE IF EXISTS {dbname}')
        cur.execute(f'CREATE DATABASE  {dbname}')
        conn.close()
        self.conn = psycopg2.connect(dbname=dbname, **params)
        self.conn.autocommit = True
        self.cur = conn.cursor()
        self.cur.execute("""
               CREATE TABLE IF NOT EXISTS default.json 
               (company_id INT NOT NULL,
               company_name VARCHAR(255) NOT NULL,
               company_url TEXT NOT NULL,
               description TEXT
               )
               """)

        cur.execute("""
               CREATE TABLE IF NOT EXISTS vacancies (
                   vacancy_id INT NOT NULL,
                   vacancy_name VARCHAR(255) NOT NULL,
                   company_name VARCHAR(255) NOT NULL,
                   salary INT,
                   vacancy_url TEXT NOT NULL,
                   description TEXT
               )
               """)

    def load_companies_data(self, company_to_find: dict):
        """
        Загружает информацию о компаниях и сохраняет в БД
        :param company_to_find: словарь компаний, где ключ это название, а значение id компании
        :return:
        """
        companies = format_companies(company_to_find)

        for company in companies:
            self.cur.execute(f"""INSERT INTO default.json (company_id, company_name, company_url, description)
                     VALUES (%s, %s, %s, %s)""", (company['company_id'], company['company_name'],
                                                  company['company_url'], company['description']))

    def load_vacancies_data(self, companies: dict):
        """
        Загружает информацию про вакансии нужных компаний
        :param companies: словарь компаний, где ключ это название, а значение id компании
        :return:
        """
        vacancies_finder = HeadHunterAPI()
        for company_id in companies.values():
            i = 0
            while i != 10:
                vacancies_finder.load_data(page=i, per_page=100, company_id=company_id)
                i += 1
        with self.conn.cursor() as cur:
            for vacancy in vacancies_finder.data:
                cur.execute(f"""INSERT INTO vacancies (vacancy_id, vacancy_name, company_name, salary, vacancy_url,
                 description) VALUES (%s, %s, %s, %s, %s, %s)""",
                            (vacancy['id'], vacancy['name'], vacancy['employer']['name'], vacancy['salary']['from'],
                             vacancy['url'], vacancy['snippet']['requirement']))

    def get_companies_and_vacancies_count(self):
        """Получить количество вакансий у каждой компании"""
        self.cur.execute("""SELECT company_name, COUNT(*) FROM vacancies GROUP BY company_name""")
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """Получить все вакансии"""
        self.cur.execute("""SELECT company_name, vacancy_name, salary, vacancy_url FROM vacancies""")
        return self.cur.fetchall()

    def get_avg_salary(self):
        """Получить среднюю зп"""
        self.cur.execute("""SELECT AVG(salary) FROM vacancies""")
        return self.cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self):
        """Поиск вакансий с зп выше среднего"""
        avg = self.get_avg_salary()
        self.cur.execute(f"""SELECT * FROM vacancies WHERE salary > {avg}""")
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str):
        """Поиск вакансий по ключевому слову"""
        self.cur.execute("""SELECT * FROM vacancies WHERE LOWER(vacancy_name) LIKE %s""", ('%'+keyword+'%',))
        return self.cur.fetchall()
