from hhapi import HeadHunterAPI
from sjapi import SuperJobAPI
from vacancy import JSONVacancyStorage, Vacancy


def user_interaction():
    """Функция взаимодействия с пользователем через терминал"""
    # Создание экземпляров классов API
    hh_api = HeadHunterAPI()
    superjob_api = SuperJobAPI()

    # Получение вакансий с разных платформ
    hh_vacancies = hh_api.get_vacancies()
    superjob_vacancies = superjob_api.get_vacancies()
    storage = JSONVacancyStorage("vacancies.json")
    for vacancy in hh_vacancies + superjob_vacancies:
        storage.save_vacancy(vacancy)

    while True:
        print("Выберите действие:")
        print("1. Получить топ N вакансий по зарплате")
        print("2. Получить вакансии в отсортированном виде")
        print("3. Получить вакансии по ключевым словам")
        print("4. Выход")
        choice = input("Введите номер действия: ")

        if choice == "1":
            n = int(input("Введите количество вакансий: "))
            # Выводим топ N вакансий по зарплате
            top_vacancies = storage.get_vacancies(lambda v: v.salary and v.salary['from'] is not None)
            top_vacancies = sorted(top_vacancies, key=lambda v: v.salary['from'], reverse=True)[:n]
            for vacancy in top_vacancies:
                print(vacancy)

        elif choice == "2":
            # Выводим вакансии в отсортированном виде
            vacancies = storage.get_vacancies(lambda v: True)
            vacancies = sorted(vacancies, key=lambda v: v.profession)
            for vacancy in vacancies:
                print(vacancy)


        elif choice == "3":
            keywords = input("Введите ключевые слова через запятую: ")
            # Выводим вакансии, содержащие указанные ключевые слова
            keywords = [keyword.strip().lower() for keyword in keywords.split(',')]
            matching_vacancies = storage.get_vacancies(
                lambda v: any(keyword in v.description.lower() for keyword in keywords))
            for vacancy in matching_vacancies:
                print(vacancy)

        elif choice == "4":
            break

        else:
            print("Некорректный выбор. Пожалуйста, выберите существующую опцию.")


user_interaction()
