import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json

def get_links(text): #функция для получения ссылок по запросу, мы передаём ей текст запроса для поиска
    ua = fake_useragent.UserAgent() #для передачи заголовка
    data = requests.get(url=f"https://hh.ru/search/vacancy?text={text}&area=1&page=1") #пишем запрос и передаём туда скопированный адрес со страницы хахару, ищем текст нашего запроса (в данном случае - python) и заменяем его на параметр функции - text
    headers = {"user-agent"} #создаём заголовок и передаём туда случайный заголовок из созданного объекта
    pass

def get_vacancies(link): #функция для получения данных вакансий, мы передаём ей ссылку
    pass

if __name__ == "__main__":
    get_links("python") #если уловие выполняется, запускаем функцию и передаём в неё текст "python"
