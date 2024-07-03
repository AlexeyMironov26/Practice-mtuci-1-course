import requests
from bs4 import BeautifulSoup
import fake_useragent
import time
import json

def get_links(text): #функция для получения ссылок по запросу, мы передаём ей текст запроса для поиска
    ua = fake_useragent.UserAgent() #для передачи заголовка
    data = requests.get(
        url=f"https://hh.ru/search/vacancy?text={text}&area=1&page=1", #пишем запрос и передаём туда скопированный адрес со страницы хахару, ищем текст нашего запроса (в данном случае - python) и заменяем его на параметр функции - text
        headers = {"user-agent":ua.random} #создаём заголовок и передаём туда случайный заголовок из созданного объекта юзер агента
    ) 
    #print(data.content) #выводим результат в консоль, в качестве результата получая содержимое страницы

    if data.status_code != 200: #если код запроса не равен 200, значит что-то пошло не так, и мы выходим из функции
        return
    thesoup = BeautifulSoup(data.content, "lxml") #передаём в эту переменную контент страницы, оборачивая его в bs


    #теперь нам нужно получить количество страниц
    try: #обернём это всё в блок try и если что то пошло не так, то мы выходим из функции
        page_amount = int(thesoup.find("div", attrs={"class": "pager"}).find_all("span", recursive=False)[-1].find("a").find("span").text) #вычленяем количество страниц из кода сайта, превращаем его в число и записывам в переменную
    except:
        return
    
    for page in range(page_amount): #делаем цикл, где для каждой страницы выполняем запрос по вытаскиванию их данных
        try:
            data = requests.get(
                url=f"https://hh.ru/search/vacancy?text={text}&area=1&page={page}", #пишем запрос и передаём туда скопированный адрес со страницы хахару, ищем текст нашего запроса (в данном случае - python) и заменяем его на параметр функции - text
                headers = {"user-agent":ua.random} #создаём заголовок и передаём туда случайный заголовок из созданного объекта юзер агента
            ) #не забываем в ссылке на место, где указан номер страницы, поставить номер страницы, на которой сейчас в данный момент цикл
            if data.status_code!=200:
                continue
            thesoup = BeautifulSoup(data.content, "lxml") #оборачиваем код каждой страницы в bs
            #извлекаем все ссылки со страницы
            for l in thesoup.find("div", attrs={"class":"vacancy-search-item__card serp-item_link vacancy-card-container--OwxCdOj5QlSlCBZvSggS"}).find("h2", attrs={"class":"bloko-header-section-2"}).find_all("a", attrs={"class":"bloko-link"}):
                yield f'{l.attrs["href"].split("?")[0]}' #мы немного редактируем каждую найденную ссылку, разделяя её сплитом по знаку вопроса и беря лишь первую часть
        except Exception as e:
            print(f"{e}")
        time.sleep(1) #чтобы не перегружать сервер

def get_vacancies(link): #функция для получения данных вакансий, мы передаём ей ссылку
    pass


if __name__ == "__main__": #данное условие, т е данный блок, кода выполняется только когда мы запускаем данный файл напрямую в качестве скрипта, а не при импорте в качестве модуля, другие же функции, которые мы писали выше могут быть импортированы и использованы в других программах в качестве модулей
    #если уловие выполняется, запускаем функцию и передаём в неё текст "python"
    for l in get_links("python"): #выводим все ссылки по данному запросу в командную строку
        print(l)
   