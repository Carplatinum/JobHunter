import logging
import os
from dotenv import load_dotenv
from typing import List

from src.api import HeadHunterAPI
from src.config import LOG_LEVEL, VACANCY_FILE, DEFAULT_PER_PAGE
from src.file_saver import JSONSaver, VacancyFileSaver
from src.utils import (
    filter_vacancies,
    get_top_vacancies,
    get_vacancies_by_salary,
    print_vacancies,
    sort_vacancies,
)
from src.vacancy import Vacancy

logging.basicConfig(level=getattr(logging, LOG_LEVEL.upper(), logging.INFO))
logger = logging.getLogger(__name__)
load_dotenv()


class VacancySaver:
    """
    Универсальный класс для сохранения вакансий в JSON или CSV в зависимости от расширения файла.
    """
    def __init__(self, filename: str) -> None:
        self.filename = filename.lower()
        self.saver: VacancyFileSaver  # объявляем тип один раз
        if self.filename.endswith('.json'):
            self.saver = JSONSaver(filename)
        elif self.filename.endswith('.csv'):
            self.saver = CSVSaver(filename)
        else:
            raise ValueError("Поддерживаются только файлы с расширением .json или .csv")

    def add_vacancy(self, vacancy: Vacancy) -> None:
        self.saver.add_vacancy(vacancy)

    def get_vacancies(self) -> List[Vacancy]:
        return self.saver.get_vacancies()

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        self.saver.delete_vacancy(vacancy)


def user_interaction() -> None:
    vacancy_file = os.getenv("VACANCY_FILE", VACANCY_FILE)
    default_per_page = int(os.getenv("DEFAULT_PER_PAGE", DEFAULT_PER_PAGE))

    hh_api = HeadHunterAPI()
    saver = VacancySaver(filename=vacancy_file)
    vacancies_list: List[Vacancy] = []

    while True:
        print("\nМеню:")
        print("1. Найти вакансии и сохранить в файл")
        print("2. Показать все сохранённые вакансии")
        print("3. Показать топ N вакансий по зарплате")
        print("4. Фильтровать вакансии по ключевому слову в описании")
        print("5. Фильтровать вакансии по диапазону зарплат")
        print("6. Удалить вакансию по названию")
        print("0. Выйти")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            query = input("Введите поисковый запрос: ").strip()
            try:
                per_page_input = input(f"Сколько вакансий загрузить (по умолчанию {default_per_page}): ").strip()
                per_page = int(per_page_input) if per_page_input else default_per_page
            except ValueError:
                per_page = default_per_page

            try:
                vacancies_json = hh_api.get_vacancies(query, per_page=per_page)
                vacancies_list = Vacancy.cast_to_object_list(vacancies_json)
                for v in vacancies_list:
                    saver.add_vacancy(v)
                print(f"Загружено и сохранено {len(vacancies_list)} вакансий.")
            except Exception as e:
                logger.error(f"Ошибка при получении вакансий: {e}")
                print(f"Ошибка при получении вакансий: {e}")

        elif choice == "2":
            vacancies = saver.get_vacancies()
            if not vacancies:
                print("Нет сохранённых вакансий.")
            else:
                print_vacancies(vacancies)

        elif choice == "3":
            vacancies = saver.get_vacancies()
            if not vacancies:
                print("Нет сохранённых вакансий.")
                continue
            try:
                top_n = int(input("Введите количество вакансий для вывода в топ N: ").strip())
            except ValueError:
                print("Некорректное число.")
                continue
            sorted_vacancies = sort_vacancies(vacancies)
            top_vacancies = get_top_vacancies(sorted_vacancies, top_n)
            print_vacancies(top_vacancies)

        elif choice == "4":
            vacancies = saver.get_vacancies()
            if not vacancies:
                print("Нет сохранённых вакансий.")
                continue
            filter_words = input("Введите ключевые слова для фильтрации (через пробел): ").strip().split()
            filtered = filter_vacancies(vacancies, filter_words)
            if filtered:
                print_vacancies(filtered)
            else:
                print("Вакансии по заданным ключевым словам не найдены.")

        elif choice == "5":
            vacancies = saver.get_vacancies()
            if not vacancies:
                print("Нет сохранённых вакансий.")
                continue
            salary_range = input("Введите диапазон зарплат (например, 100000-150000): ").strip()
            ranged = get_vacancies_by_salary(vacancies, salary_range)
            if ranged:
                print_vacancies(ranged)
            else:
                print("Вакансии в заданном диапазоне зарплат не найдены.")

        elif choice == "6":
            vacancies = saver.get_vacancies()
            if not vacancies:
                print("Нет сохранённых вакансий.")
                continue
            title = input("Введите точное название вакансии для удаления: ").strip()
            found = [v for v in vacancies if v.title == title]
            if not found:
                print("Вакансия не найдена.")
            else:
                for v in found:
                    saver.delete_vacancy(v)
                print("Вакансия удалена.")

        elif choice == "0":
            print("Выход.")
            break

        else:
            print("Некорректный выбор. Повторите попытку.")


if __name__ == "__main__":
    user_interaction()
