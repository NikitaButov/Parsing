import requests

from jobsite import JobSiteAPI
from vacancy import Vacancy


class SuperJobAPI(JobSiteAPI):
    """
               Класс по получению вакансий с сайта SuperJob.
               """
    def __init__(self):
        self.api_key = 'v3.r.137808305.7e48422acf0ab05c530b509558a36a4f025b37a5' \
                       '.55e25d85968842f713673f320a36e63cc5527eeb'

    def get_vacancies(self):
        """
                Поключение к сайти и копирование вакансий с сайта
                """
        url = 'https://api.superjob.ru/2.0/vacancies'
        headers = {
            'X-Api-App-Id': self.api_key
        }
        payload = {
            'text': "python",
            'page': 0,
        }

        response = requests.get(url, params=payload, headers=headers)
        js_data = response.json()
        vacancies = []
        for line in js_data['objects']:
            link = line['link']
            profession = line['profession']
            salary = {
                'from': line['payment_from'],
                'to': line['payment_to'],
                'currency': line['currency']
            }
            description = line['vacancyRichText']
            vec = Vacancy(profession, salary, link, description)
            vacancies.append(vec)
        return vacancies
