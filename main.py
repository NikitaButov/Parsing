from hhapi import HeadHunterAPI
from sjapi import SuperJobAPI
from vacancy import JSONVacancyStorage, Vacancy


def interact():
    hh_client_id = 'I88OP6RS2118MDVUKBI6K8CMLEGGSSFMQA5MJFTDIO9KINUC7DIH5GU4M4CLP6L2'
    hh_client_secret = 'IG4JQSGDOL3SRT0N3KT94U5D1NV5CAM03MUC49Q9VNU84VFLJ6INHFN9U9QB3FBC'

    hh_api = HeadHunterAPI(hh_client_id, hh_client_secret)
    hh_api.connect()

    superjob_token = 'v3.r.137808305.7e48422acf0ab05c530b509558a36a4f025b37a5.55e25d85968842f713673f320a36e63cc5527eeb'
    superjob_api = SuperJobAPI(superjob_token)
    superjob_api.connect()

    storage = JSONVacancyStorage('vacancies.json')

    while True:
        print('1. Поиск вакансий')
        print('2. Добавить вакансию')
        print('3. Удалить вакансию')
        print('4. Получить вакансии с определенными ключевыми словами в описании')
        print('5. Получить топ N вакансий по зарплате')
        print('6. Получить вакансии в отсортированном виде')
        print('7. Выйти')

        choice = input('Выберите действие: ')

        if choice == '1':
            query = input('Введите поисковый запрос: ')
            hh_vacancies = hh_api.get_vacancies(query)
            superjob_vacancies = superjob_api.get_vacancies(query)
            all_vacancies = hh_vacancies + superjob_vacancies

            for vacancy_data in all_vacancies:
                title = vacancy_data['title']
                salary = vacancy_data['salary']
                description = vacancy_data['description']
                link = vacancy_data['link']
                vacancy = Vacancy(title, salary, description, link)
                storage.save_vacancy(vacancy)
            print('Вакансии сохранены')
        elif choice == '2':
            title = input('Введите название вакансии: ')
            salary = input('Введите зарплату: ')
            description = input('Введите описание: ')
            link = input('Введите ссылку на вакансию: ')
            vacancy = Vacancy(title, salary, description, link)
            storage.save_vacancy(vacancy)
            print('Вакансия добавлена')
        elif choice == '3':
            title = input('Введите название вакансии: ')
            salary = input('Введите зарплату: ')
            description = input('Введите описание: ')
            link = input('Введите ссылку на вакансию: ')
            vacancy = Vacancy(title, salary, description, link)
            if storage.delete_vacancy(vacancy):
                print('Вакансия удалена')
            else:
                print('Вакансия не найдена')
        elif choice == '4':
            keyword = input('Введите ключевое слово для поиска: ')
            vacancies = storage.get_vacancies(description=keyword)
            for vacancy in vacancies:
                print(vacancy)
        elif choice == '5':
            n = int(input('Введите количество вакансий: '))
            vacancies = storage.get_vacancies()
            vacancies.sort(key=lambda v: v.salary, reverse=True)
            for i, vacancy in enumerate(vacancies[:n]):
                print(f'{i + 1}. {vacancy}')
        elif choice == '6':
            vacancies = storage.get_vacancies()
            vacancies.sort(key=lambda v: v.salary, reverse=True)
            for vacancy in vacancies:
                print(vacancy)
        elif choice == '7':
            break
        else:
            print('Неверный выбор')

# if __name__ == '__main__':
#     storage = JSONVacancyStorage('vacancies.json')
#     interact()
