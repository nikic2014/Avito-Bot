import requests
from bs4 import BeautifulSoup
import time


def check_status_cod(page, link):
    if page.status_code < 200 or page.status_code > 299:
        print("Неизвестное состояние запроса.")
        print("Link:", link, page.status_code)
    time.sleep(10)


main_URL = "https://www.avito.ru/"


def parse_car():
    URL = "https://www.avito.ru/saratov/avtomobili?cd=1&radius=50&searchRadius=50"
    page = requests.get(URL, headers={
        'proxy' : '134.236.147.134:5678'})
    check_status_cod(page, URL)

    soup = BeautifulSoup(page.content, "html.parser")

    links = soup.findAll("a",
                         class_="link-link-MbQDP "
                                "link-design-default-_nSbv "
                                "title-root-zZCwT iva-item-title-py3i_ "
                                "title-listRedesign-_rejR "
                                "title-root_maxHeight-X6PsH")

    for i in links:
        URL_current_car = main_URL + i["href"]
        print(URL_current_car)
        page_current_car = requests.get(URL_current_car)
        check_status_cod(page_current_car, URL_current_car)

        soup_for_car = BeautifulSoup(page_current_car.content, "html.parser")
        title = soup_for_car.find("span", class_="title-info-title-text")
        print(title)


parse_car()


def test_parse():
    URL = "https://www.avito.ru/engels/avtomobili/chevrolet_aveo_2011_2761454879"
    page = requests.get(URL)

    check_status_cod(page, URL)

    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find("span", class_="title-info-title-text")

    print(title.text)

test_parse()
