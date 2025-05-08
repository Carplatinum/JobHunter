from abc import ABC, abstractmethod
from typing import Any, Dict, List
import requests
import logging
from src.config import HH_API_URL
import json

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class VacancyAPI(ABC):
    """
    Абстрактный класс для работы с API сервисов вакансий.
    """

    @abstractmethod
    def _connect(self) -> None:
        """
        Метод для подключения к API.
        """
        pass

    @abstractmethod
    def get_vacancies(self, keyword: str, per_page: int = 20) -> List[Dict[str, Any]]:
        """
        Получить вакансии по ключевому слову.
        """
        pass


class HeadHunterAPI(VacancyAPI):
    """
    Класс для работы с API hh.ru.
    """

    __BASE_URL = HH_API_URL

    def __init__(self) -> None:
        self.__session = requests.Session()

    def _connect(self) -> None:
        """
        Метод подключения к API hh.ru.
        Отправляет тестовый запрос и проверяет статус ответа.
        """
        params: dict[str, str | int] = {'text': 'python', 'per_page': 1}
        response = self.__session.get(self.__BASE_URL, params=params)  # type: ignore[arg-type]
        if response.status_code != 200:
            raise ConnectionError("Не удалось подключиться к API hh.ru")

    def get_vacancies(self, keyword: str, per_page: int = 20) -> List[Dict[str, Any]]:
        """
        Получить список вакансий по ключевому слову с hh.ru.
        Вызывает метод подключения перед запросом.
        Обрабатывает ошибки JSON и логирует ответ при ошибке.
        """
        self._connect()
        params: dict[str, str | int] = {
            'text': keyword,
            'per_page': per_page,
            'area': 113  # Россия
        }
        response = self.__session.get(self.__BASE_URL, params=params)  # type: ignore[arg-type]
        if response.status_code != 200:
            raise RuntimeError("Ошибка получения данных с hh.ru")

        try:
            data = response.json()
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка декодирования JSON: {e}")
            logger.error(f"Ответ сервера (первые 1000 символов): {response.text[:1000]}")
            raise RuntimeError("Ошибка получения данных с hh.ru (невалидный JSON)")

        return data.get('items', [])
