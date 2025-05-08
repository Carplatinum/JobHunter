from typing import List

import pytest

from src.utils import (filter_vacancies, get_top_vacancies,
                       get_vacancies_by_salary, print_vacancies,
                       sort_vacancies)
from src.vacancy import Vacancy


@pytest.fixture
def sample_vacancies() -> List[Vacancy]:
    """
    Фикстура, создающая список тестовых вакансий.
    """
    return [
        Vacancy("Python Developer", "url1", 150000, "Опыт с Django и Flask"),
        Vacancy("Junior Developer", "url2", 80000, "Начинающий специалист"),
        Vacancy("QA Engineer", "url3", 90000, "Тестирование, автоматизация"),
        Vacancy("Data Scientist", "url4", 200000, "Опыт работы с ML и Python"),
    ]


def test_filter_vacancies(sample_vacancies: List[Vacancy]) -> None:
    """
    Проверяет фильтрацию вакансий по ключевым словам.
    """
    keywords = ["django", "ml"]
    filtered = filter_vacancies(sample_vacancies, keywords)
    titles = [v.title for v in filtered]
    assert "Python Developer" in titles
    assert "Data Scientist" in titles
    assert len(filtered) == 2


def test_filter_vacancies_no_match(sample_vacancies: List[Vacancy]) -> None:
    """
    Проверяет, что при отсутствии совпадений возвращается пустой список.
    """
    filtered = filter_vacancies(sample_vacancies, ["java"])
    assert filtered == []


def test_get_vacancies_by_salary(sample_vacancies: List[Vacancy]) -> None:
    """
    Проверяет фильтрацию вакансий по диапазону зарплат.
    """
    salary_range = "85000-160000"
    filtered = get_vacancies_by_salary(sample_vacancies, salary_range)
    titles = [v.title for v in filtered]
    assert "Python Developer" in titles
    assert "QA Engineer" in titles
    assert "Junior Developer" not in titles
    assert "Data Scientist" not in titles


def test_get_vacancies_by_salary_invalid_range(sample_vacancies: List[Vacancy]) -> None:
    """
    Проверяет поведение при некорректном формате диапазона зарплат.
    """
    filtered = get_vacancies_by_salary(sample_vacancies, "invalid-range")
    assert filtered == sample_vacancies


def test_sort_vacancies(sample_vacancies: List[Vacancy]) -> None:
    """
    Проверяет сортировку вакансий по убыванию зарплаты.
    """
    sorted_v = sort_vacancies(sample_vacancies)
    salaries = [v.salary for v in sorted_v]
    assert salaries == sorted(salaries, reverse=True)


def test_get_top_vacancies(sample_vacancies: List[Vacancy]) -> None:
    """
    Проверяет получение топ-N вакансий.
    """
    sorted_v = sort_vacancies(sample_vacancies)
    top_2 = get_top_vacancies(sorted_v, 2)
    assert len(top_2) == 2
    assert top_2[0].salary >= top_2[1].salary


def test_print_vacancies(capsys: pytest.CaptureFixture, sample_vacancies: List[Vacancy]) -> None:
    """
    Проверяет вывод вакансий в консоль.
    """
    print_vacancies(sample_vacancies[:1])
    captured = capsys.readouterr()
    assert "Python Developer" in captured.out
    assert "Опыт с Django и Flask" in captured.out
