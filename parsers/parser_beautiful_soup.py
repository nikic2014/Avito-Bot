import requests
from bs4 import BeautifulSoup
import time


def check_status_cod(page, link):
    if page.status_code < 200 or page.status_code > 299:
        print("Неизвестное состояние запроса.")
        print("Link:", link, page.status_code)
    else:
        print(page.status_code)

    time.sleep(10)


def parse_current_car(URL):
    page = requests.get(URL)
    check_status_cod(page, URL)

    soup = BeautifulSoup(page.content, "html.parser")
    title = soup.find("span", class_="title-info-title-text")
    print(title.text)
    price = soup.find("span", class_="style-price-value-main-TIg6u").find_next()
    print(price.text)
    link = URL
    print(link)
    try:
        description = soup.find("div",
                                class_="style-item-description-html-qCwUL").find_next()
        print(description.text)

        return (title.text, price.text, description.text)
    except:
        description = soup.find("div",
                                class_="style-item-description-text-mc3G6").find_next()
        print(description.text)

        return (title.text, price.text, description.text)