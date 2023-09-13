import requests

from jobsite import JobSiteAPI


class SuperJobAPI(JobSiteAPI):
    def __init__(self, token):
        super().__init__(token)

    def connect(self):
        print('Подключено к API SuperJob')

    def get_vacancies(self, query):
        url = 'https://api.superjob.ru/2.0/vacancies'
        headers = {
            'X-Api-App-Id': self.token
        }
        params = {
            'keyword': query,
            'town': 4  # Значение 4 соответствует Москве
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            vacancies = response.json()['objects']
            return vacancies
        else:
            return []