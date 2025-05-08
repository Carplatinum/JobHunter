import json
import os
import csv
from abc import ABC, abstractmethod
from typing import List

from src.config import VACANCY_FILE
from src.vacancy import Vacancy


class VacancyFileSaver(ABC):
    """Абстрактный класс для работы с файлами вакансий."""

    @abstractmethod
    def add_vacancy(self, vacancy: Vacancy) -> None:
        pass

    @abstractmethod
    def get_vacancies(self) -> List[Vacancy]:
        pass

    @abstractmethod
    def delete_vacancy(self, vacancy: Vacancy) -> None:
        pass


class JSONSaver(VacancyFileSaver):
    """Класс для работы с JSON-файлом вакансий."""

    def __init__(self, filename: str = VACANCY_FILE) -> None:
        self.__filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            self._save_to_file(vacancies)

    def get_vacancies(self) -> List[Vacancy]:
        if not os.path.exists(self.__filename):
            return []
        with open(self.__filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            return [Vacancy(**item) for item in data]

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v != vacancy]
        self._save_to_file(vacancies)

    def _save_to_file(self, vacancies: List[Vacancy]) -> None:
        with open(self.__filename, "w", encoding="utf-8") as f:
            json.dump([v.as_dict() for v in vacancies], f, ensure_ascii=False, indent=2)


class CSVSaver(VacancyFileSaver):
    """Класс для работы с CSV-файлом вакансий."""

    def __init__(self, filename: str = "data/vacancies.csv") -> None:
        self.__filename = filename

    def add_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        if vacancy not in vacancies:
            vacancies.append(vacancy)
            self._save_to_file(vacancies)

    def get_vacancies(self) -> List[Vacancy]:
        if not os.path.exists(self.__filename):
            return []
        vacancies = []
        with open(self.__filename, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                salary = 0
                try:
                    salary = int(row.get('salary', '0'))
                except ValueError:
                    pass
                vacancy = Vacancy(
                    title=row.get('title', ''),
                    url=row.get('url', ''),
                    salary=salary,
                    description=row.get('description', '')
                )
                vacancies.append(vacancy)
        return vacancies

    def delete_vacancy(self, vacancy: Vacancy) -> None:
        vacancies = self.get_vacancies()
        vacancies = [v for v in vacancies if v != vacancy]
        self._save_to_file(vacancies)

    def _save_to_file(self, vacancies: List[Vacancy]) -> None:
        with open(self.__filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['title', 'url', 'salary', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for v in vacancies:
                writer.writerow(v.as_dict())
