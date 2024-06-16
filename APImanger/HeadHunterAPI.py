from APImanger import IApi
import requests


class HeadHunterAPI(IApi.IApi):
    """
    Класс для работы с API HH.ru
    """
    __slots__ = ('urls', 'vacancies', '__data')

    def __init__(self):
        super().__init__()
        self.vacancies = None
        self.urls = {"vacancies": "https://api.hh.ru/vacancies"}
        self.__data = []

    def load_data(self, search="", page=0, per_page=1, company_id=None):
        """
        Метод загрузки данных с сайта HH.ru
        :param company_id: id компании чьи вакансии требуется найти.
        :param search: Поисковый запрос по которому будут отбираться вакансии
        :param page: страница с вакансиями
        :param per_page: сколько требуется загрузить вакансий на странице
        :return: код выполнения загрузки
        """
        if company_id is None:
            self.vacancies = requests.get(self.urls['vacancies'],
                                          params={"text": search, "only_with_salary": True, "page": page,
                                                  "per_page": per_page, "currency": "RUR"})
            self.__data.extend(self.vacancies.json()['items'])
            return self.vacancies.status_code
        else:
            self.vacancies = requests.get(self.urls['vacancies'] + f'?employer_id={company_id}',
                                          params={"text": search, "only_with_salary": True, "page": page,
                                                  "per_page": per_page, "currency": "RUR"})
            self.__data.extend(self.vacancies.json()['items'])
            return self.vacancies.status_code

    @staticmethod
    def find_companies(name, only_with_vacancies=True):
        """
        Метод поиска работодателей
        :param name: описание по которому нужно сделать выборку.
        :param only_with_vacancies: Параметр по которому осуществляется поиск работодателей только
         с открытыми вакансиями.
        :return: Словарь с работодателями.
        """
        companies = requests.get('https://api.hh.ru/employers', params={"text": name,
                                                                        'only_with_vacancies': only_with_vacancies})
        return companies.json()['items']

    @property
    def data(self):
        return self.__data
