import json
from abc import abstractmethod, ABC


class Vacancy:
    def __init__(self, profession, salary, link, description):
        """
                Класс, представляющий вакансию

                Args:
                    profession (str): Название профессии
                    salary (dict): Информация о зарплате
                    link (str): Ссылка на вакансию
                    description (str): Описание вакансии
                """
        self.profession = profession
        self.salary = salary
        self.description = description
        self.link = link

    def format_salary(self):
        if not self.salary:
            return "Не указана"
        from_value = self.salary.get('from', '')
        to_value = self.salary.get('to', '')
        currency = self.salary.get('currency', '')

        if from_value and to_value:
            """
                   Форматирование информации о зарплате
                   """
            salary_range = f"От {from_value} до {to_value} {currency}"
        elif from_value:
            salary_range = f"От {from_value} {currency}"
        elif to_value:
            salary_range = f"До {to_value} {currency}"
        else:
            salary_range = "Не указана"

        return salary_range

    def __repr__(self):
        return f'{self.profession}\nЗарплата: {self.format_salary()}\nОписание: {self.description}\nСсылка: {self.link}\n'


class VacancyStorage(ABC):
    @abstractmethod
    def save_vacancy(self, vacancy):
        pass

    @abstractmethod
    def get_vacancies(self, criteria):
        pass

    @abstractmethod
    def remove_vacancy(self, vacancy):
        pass


class JSONVacancyStorage(VacancyStorage):
    """
            Хранилище вакансий в формате JSON
            """
    def __init__(self, file_name):
        self.file_name = file_name

    def save_vacancy(self, vacancy):
        """
        Сохраняет вакансию в формате JSON
        """
        with open(self.file_name, 'a', encoding="utf-8") as file:
            json.dump(vars(vacancy), file, ensure_ascii=False)
            file.write('\n')

    def get_vacancies(self, criteria):
        """
                Возвращает список вакансий, удовлетворяющих заданным критериям
                """
        with open(self.file_name, 'r', encoding="utf-8") as file:
            vacancies = []
            for line in file:
                vacancy_data = json.loads(line)
                vacancy = Vacancy(**vacancy_data)
                if criteria(vacancy):
                    vacancies.append(vacancy)
            return vacancies

    def remove_vacancy(self, vacancy):
        with open(self.file_name, 'r+', encoding="utf-8") as file:
            lines = file.readlines()
            file.seek(0)
            for line in lines:
                vacancy_data = json.loads(line)
                existing_vacancy = Vacancy(**vacancy_data)
                if existing_vacancy != vacancy:
                    file.write(line)
            file.truncate()
