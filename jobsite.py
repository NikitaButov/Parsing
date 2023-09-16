from abc import ABC, abstractmethod


class JobSiteAPI(ABC):
    @abstractmethod
    def get_vacancies(self):
        pass