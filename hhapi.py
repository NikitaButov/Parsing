import pprint

import requests

from jobsite import JobSiteAPI
from vacancy import Vacancy


class HeadHunterAPI(JobSiteAPI):
    def __init__(self):
        pass

    def get_vacancies(self):
        payload = {
            'text': "python",
            'page': 0,
        }

        url = 'https://api.hh.ru/vacancies'
        request = requests.get(url, payload)
        js_data = request.json()
        vacancys = []
        for line in js_data['items']:
            link = line['url'],
            profession = line['name'],
            salary = line['salary'].get('from', 0),
            description = line['snippet']['responsibility']
            vec = Vacancy(profession, salary, link, description)
            vacancys.append(vec)

        return vacancys


hh = HeadHunterAPI()

hh_get = hh.get_vacancies()
pprint.pprint(hh_get)
