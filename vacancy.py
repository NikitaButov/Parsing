import json
from abc import abstractmethod, ABC


class Vacancy:
    def __init__(self, title, salary, link, description):
        self.title = title
        self.salary = salary
        self.description = description
        self.link = link

    def __str__(self):
        return f'{self.title}\nЗарплата: {self.salary}\nОписание: {self.description}\nСсылка: {self.link}\n'


class VacancyStorage(ABC):
    @abstractmethod
    def save_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, **kwargs):
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy):
        pass


class JSONVacancyStorage(VacancyStorage):
    def __init__(self, filename):
        self.filename = filename
        self.vacancies = []

    def save_vacancy(self, vacancy):
        self.vacancies.append(vacancy)
        with open(self.filename, 'w') as f:
            json.dump([{
                'title': v.title,
                'salary': v.salary,
                'description': v.description,
                'link': v.link
            } for v in self.vacancies], f, indent=4)

    def get_vacancies(self, **kwargs):
        with open(self.filename, 'r') as f:
            self.vacancies = [Vacancy(**v) for v in json.load(f)]

        if kwargs:
            filtered_vacancies = []
            for vacancy in self.vacancies:
                valid = True
                for key, value in kwargs.items():
                    if getattr(vacancy, key, None) != value:
                        valid = False
                        break
                if valid:
                    filtered_vacancies.append(vacancy)
            return filtered_vacancies
        else:
            return self.vacancies

    def delete_vacancy(self, vacancy):
        self.vacancies.remove(vacancy)
        with open(self.filename, 'w') as f:
            json.dump([{
                'title': v.title,
                'salary': v.salary,
                'description': v.description,
                'link': v.link
            } for v in self.vacancies], f, indent=4)
