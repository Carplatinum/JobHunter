import os

from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env в окружение

VACANCY_FILE = os.getenv("VACANCY_FILE", "data/vacancies.json")
DEFAULT_PER_PAGE = int(os.getenv("DEFAULT_PER_PAGE", 20))
HH_API_URL = os.getenv("HH_API_URL", "https://dev.hh.ru/")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
