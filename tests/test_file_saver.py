import os
import pytest
from typing import Generator
from src.vacancy import Vacancy
from src.file_saver import JSONSaver, CSVSaver


@pytest.fixture
def sample_vacancy() -> Vacancy:
    """Создаёт пример объекта Vacancy для тестов."""
    return Vacancy(
        title="Python Developer",
        url="https://hh.ru/vacancy/123",
        salary=100000,
        description="Разработка на Python"
    )


@pytest.fixture
def temp_json_file() -> Generator[str, None, None]:
    """Создаёт временный JSON-файл и удаляет его после теста."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
        filename = f.name
    yield filename
    if os.path.exists(filename):
        os.remove(filename)


@pytest.fixture
def temp_csv_file() -> Generator[str, None, None]:
    """Создаёт временный CSV-файл и удаляет его после теста."""
    import tempfile
    with tempfile.NamedTemporaryFile(mode='w+', suffix='.csv', delete=False) as f:
        filename = f.name
    yield filename
    if os.path.exists(filename):
        os.remove(filename)


def test_json_saver_add_get_delete(sample_vacancy: Vacancy, temp_json_file: str) -> None:
    """Тестирует добавление, получение и удаление вакансий в JSONSaver."""
    saver = JSONSaver(filename=temp_json_file)

    assert saver.get_vacancies() == []

    saver.add_vacancy(sample_vacancy)
    vacancies = saver.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].title == sample_vacancy.title

    saver.add_vacancy(sample_vacancy)  # дубликат не добавится
    vacancies = saver.get_vacancies()
    assert len(vacancies) == 1

    saver.delete_vacancy(sample_vacancy)
    assert saver.get_vacancies() == []


def test_csv_saver_add_get_delete(sample_vacancy: Vacancy, temp_csv_file: str) -> None:
    """Тестирует добавление, получение и удаление вакансий в CSVSaver."""
    saver = CSVSaver(filename=temp_csv_file)

    assert saver.get_vacancies() == []

    saver.add_vacancy(sample_vacancy)
    vacancies = saver.get_vacancies()
    assert len(vacancies) == 1
    assert vacancies[0].title == sample_vacancy.title

    saver.add_vacancy(sample_vacancy)  # дубликат не добавится
    vacancies = saver.get_vacancies()
    assert len(vacancies) == 1

    saver.delete_vacancy(sample_vacancy)
    assert saver.get_vacancies() == []
