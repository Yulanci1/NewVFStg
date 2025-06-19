
import requests
from bs4 import BeautifulSoup

CITIES = [
    "Москва", "Санкт-Петербург", "Екатеринбург", "Новосибирск", "Казань", "Самара",
    "Ростов-на-Дону", "Нижний Новгород", "Краснодар", "Уфа", "Пермь", "Омск",
]

def check_slots():
    result = {}
    for city in CITIES:
        # Имитация запроса
        available = False  # замените на реальную проверку
        result[city] = available
    return result
