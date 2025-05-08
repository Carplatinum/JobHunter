from typing import Any, Dict, List

from src.vacancy import Vacancy


def test_vacancy_initialization_and_properties() -> None:
    """
    Проверяет корректную инициализацию и свойства объекта Vacancy.
    """
    vac = Vacancy("Developer", "http://example.com", 120000, "Some description")
    assert vac.title == "Developer"
    assert vac.url == "http://example.com"
    assert vac.salary == 120000
    assert vac.description == "Some description"


def test_vacancy_validation_defaults() -> None:
    """
    Проверяет, что при некорректных или пустых данных выставляются значения по умолчанию.
    """
    vac = Vacancy("", "", 0, "")
    assert vac.title == "Без названия"
    assert vac.url == "Нет ссылки"
    assert vac.salary == 0
    assert vac.description == "Нет описания"


def test_vacancy_comparisons() -> None:
    """
    Проверяет работу методов сравнения вакансий по зарплате.
    """
    vac1 = Vacancy("A", "url1", 100000, "desc")
    vac2 = Vacancy("B", "url2", 150000, "desc")
    vac3 = Vacancy("C", "url3", 100000, "desc")

    assert vac1 < vac2
    assert vac2 > vac1
    assert vac1 == vac3
    assert (vac1 == "not a vacancy") is False  # __eq__ с несовместимым типом возвращает NotImplemented -> False


def test_as_dict_returns_correct_dict() -> None:
    """
    Проверяет, что метод as_dict возвращает словарь с правильными данными.
    """
    vac = Vacancy("Dev", "url", 50000, "desc")
    d = vac.as_dict()
    assert isinstance(d, dict)
    assert d["title"] == "Dev"
    assert d["url"] == "url"
    assert d["salary"] == 50000
    assert d["description"] == "desc"


def test_cast_to_object_list_creates_vacancies() -> None:
    """
    Проверяет, что метод cast_to_object_list корректно создает список объектов Vacancy из списка словарей.
    """
    input_data: List[Dict[str, Any]] = [
        {
            "name": "Dev",
            "alternate_url": "url1",
            "salary": {"from": 100000},
            "snippet": {"requirement": "req1"}
        },
        {
            "name": "QA",
            "alternate_url": "url2",
            "salary": None,
            "snippet": {"responsibility": "resp2"}
        }
    ]
    vacancies = Vacancy.cast_to_object_list(input_data)
    assert len(vacancies) == 2
    assert vacancies[0].title == "Dev"
    assert vacancies[0].salary == 100000
    assert vacancies[0].description == "req1"
    assert vacancies[1].title == "QA"
    assert vacancies[1].salary == 0  # зарплата не указана
    assert vacancies[1].description == "resp2"
