from unittest.mock import MagicMock, patch
import pytest
from src.api import HeadHunterAPI


@patch("src.api.requests.Session.get")
def test_get_vacancies_success(mock_get) -> None:
    """
    Проверяет успешное получение вакансий с hh.ru через HeadHunterAPI.
    """
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "items": [
            {
                "name": "Python Dev",
                "alternate_url": "url",
                "salary": {"from": 100000},
                "snippet": {"requirement": "Python"}
            },
            {
                "name": "QA",
                "alternate_url": "url2",
                "salary": {"from": 80000},
                "snippet": {"requirement": "Test"}
            }
        ]
    }
    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    vacancies = api.get_vacancies("Python", per_page=2)
    assert isinstance(vacancies, list)
    assert len(vacancies) == 2
    assert vacancies[0]["name"] == "Python Dev"
    assert vacancies[1]["salary"]["from"] == 80000


@patch("src.api.requests.Session.get")
def test_get_vacancies_api_error(mock_get) -> None:
    """
    Проверяет обработку ошибки при неудачном подключении к API hh.ru.
    """
    mock_response = MagicMock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    api = HeadHunterAPI()
    with pytest.raises(ConnectionError):
        api._connect()
    with pytest.raises(ConnectionError):
        api.get_vacancies("Python")
