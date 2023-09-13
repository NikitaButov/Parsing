from abc import ABC, abstractmethod


class JobSiteAPI(ABC):
    def __init__(self, token):
        self.token = token

    @abstractmethod
    def get_vacancies(self, query):
        pass