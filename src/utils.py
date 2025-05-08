from typing import List

from src.vacancy import Vacancy


def filter_vacancies(vacancies: List[Vacancy], keywords: List[str]) -> List[Vacancy]:
    """
    Фильтрует список вакансий, оставляя только те, в описании которых есть хотя бы одно из ключевых слов.
    """
    result: List[Vacancy] = []
    for v in vacancies:
        if any(word.lower() in v.description.lower() for word in keywords):
            result.append(v)
    return result


def get_vacancies_by_salary(vacancies: List[Vacancy], salary_range: str) -> List[Vacancy]:
    """
    Фильтрует вакансии по заданному диапазону зарплат.
    """
    try:
        min_salary, max_salary = map(int, salary_range.replace(' ', '').split('-'))
    except Exception:
        # Если формат некорректный, возвращаем исходный список без фильтрации
        return vacancies
    return [v for v in vacancies if min_salary <= v.salary <= max_salary]


def sort_vacancies(vacancies: List[Vacancy]) -> List[Vacancy]:
    """
    Сортирует вакансии по зарплате в порядке убывания.
    """
    return sorted(vacancies, reverse=True)


def get_top_vacancies(vacancies: List[Vacancy], top_n: int) -> List[Vacancy]:
    """
    Возвращает топ N вакансий из списка.
    """
    return vacancies[:top_n]


def print_vacancies(vacancies: List[Vacancy]) -> None:
    """
    Выводит список вакансий в удобочитаемом формате в консоль.
    """
    for v in vacancies:
        print(
            f"Название: {v.title}\n"
            f"Ссылка: {v.url}\n"
            f"Зарплата: {v.salary}\n"
            f"Описание: {v.description}\n"
            f"{'-'*40}"
        )
