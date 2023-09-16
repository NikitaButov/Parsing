import requests

from jobsite import JobSiteAPI
from vacancy import Vacancy


class HeadHunterAPI(JobSiteAPI):
    """
           Класс по получению вакансий с сайта HeadHunter.
           """
    def __init__(self):
        super().__init__()

    def get_vacancies(self):
        """
        Поключение к сайти и копирование вакансий с сайта
        """
        payload = {
            'text': "python",
            'page': 0,
        }

        url = 'https://api.hh.ru/vacancies'
        response = requests.get(url, params=payload)
        js_data = response.json()
        vacancies = []
        for line in js_data['items']:
            link = line['alternate_url']
            profession = line['name']
            salary = line.get('salary', {})
            description = line['snippet']['responsibility']
            vec = Vacancy(profession, salary, link, description)
            vacancies.append(vec)

        return vacancies
