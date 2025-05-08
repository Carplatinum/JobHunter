from typing import Any, Dict, List


class Vacancy:
    """
    Класс для представления вакансии.
    """
    __slots__ = ('__title', '__url', '__salary', '__description')

    def __init__(self, title: str, url: str, salary: int, description: str):
        self.__title = self.__validate_title(title)
        self.__url = self.__validate_url(url)
        self.__salary = self.__validate_salary(salary)
        self.__description = self.__validate_description(description)

    @staticmethod
    def __validate_title(title: str) -> str:
        return title.strip() if title else "Без названия"

    @staticmethod
    def __validate_url(url: str) -> str:
        return url.strip() if url else "Нет ссылки"

    @staticmethod
    def __validate_salary(salary: Any) -> int:
        try:
            return int(salary)
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def __validate_description(description: str) -> str:
        return description.strip() if description else "Нет описания"

    @property
    def title(self) -> str:
        return self.__title

    @property
    def url(self) -> str:
        return self.__url

    @property
    def salary(self) -> int:
        return self.__salary

    @property
    def description(self) -> str:
        return self.__description

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def __gt__(self, other: object) -> bool:
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary > other.salary

    def as_dict(self) -> Dict[str, Any]:
        """
        Представление вакансии в виде словаря.
        """
        return {
            "title": self.title,
            "url": self.url,
            "salary": self.salary,
            "description": self.description
        }

    @classmethod
    def cast_to_object_list(cls, vacancies: List[Dict[str, Any]]) -> List['Vacancy']:
        """
        Преобразует список словарей в список объектов Vacancy.
        """
        result = []
        for v in vacancies:
            salary = 0
            if v.get('salary') and v['salary'].get('from'):
                salary = v['salary']['from']
            result.append(
                cls(
                    v.get('name', ''),
                    v.get('alternate_url', ''),
                    salary,
                    v.get('snippet', {}).get('requirement', '') or v.get('snippet', {}).get('responsibility', '')
                )
            )
        return result
