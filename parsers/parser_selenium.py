import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium_stealth import stealth
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

import database
from database import Cars_ads, Images_cars

option = webdriver.ChromeOptions()
option.add_argument("start-maximized")
option.add_experimental_option("excludeSwitches", ["enable-automation"])
option.add_experimental_option("useAutomationExtension", False)
driver = webdriver.Chrome(options=option)


def parse_info(URL):
    print("Зашли в функцию парсинга информации о новых объявлениях")
    print(f"Получаем данные о машине: {URL}")

    browser = driver
    browser.get(URL)

    img_array = []

    title = browser.find_element(By.CLASS_NAME,
                                 "title-info-title-text").get_attribute(
        "innerHTML")

    description = ""
    try:
        description = browser.find_element(By.CLASS_NAME,
                                           "style-item-description"
                                           "-text-mc3G6").find_element(
            By.TAG_NAME, "p").get_attribute("innerHTML")
    except:
        try:
            p = browser.find_element(By.CLASS_NAME,
                                     "style-item-description"
                                     "-html-qCwUL").find_elements(
                By.TAG_NAME, "p")

            for i in p:
                description += i.get_attribute("innerHTML")
        except:
            description = browser.find_element(By.CLASS_NAME,
                                               "style-item-description"
                                               "-html-qCwUL").get_attribute(
                "innerHTML")

    price = browser.find_element(By.CLASS_NAME,
                                 "style-price-value-main-TIg6u").find_element(
        By.TAG_NAME, "span").get_attribute("content")

    while 1:
        try:
            class_image = browser.find_element(By.CLASS_NAME,
                                               "image-frame-wrapper-_NvbY")
            tag_image = class_image.find_element(By.TAG_NAME, "img")
            link_image = tag_image.get_attribute("src")
            if link_image in img_array:
                break
            img_array.append(link_image)
        except:
            break

        try:
            btn = browser.find_elements(By.CLASS_NAME,
                                        "image-frame-controlButton-_vPNK")
            btn[1].click()
            time.sleep(0.5)
        except:
            return []

    return (img_array, title, price, description)


def test_parse(URL, l):
    print("Зашли в функцию пасинга списка объявлений")
    browser = driver
    browser.get(URL)

    last = browser.find_elements(By.CLASS_NAME, "pagination-item-JJq_j")
    last = int(last[-2].get_attribute("innerHTML"))
    for page in range(1, last + 1):
        try:
            URL = str(URL).replace("p=", f"p={page}")
            print(f"Находимся на странице: {page}")

            browser.get(URL)
            time.sleep(5)

            links = []
            cars = browser.find_elements(By.CLASS_NAME,
                                         "iva-item-titleStep-pdebR")
            for i in cars:
                link = i.find_element(By.TAG_NAME, "a").get_attribute("href")

                s = select(Cars_ads).where(Cars_ads.link == link)
                result = database.get_cars(s, l)

                if result == []:
                    links.append(link)

            browser.quit()

            for i in links:
                info = parse_info(i)
                if info == []:
                    print(
                        "Машина или продана, или в ее "
                        "изображениях встретилось видео",
                        i)
                    time.sleep(3)
                    continue

                ins = database.insert(Cars_ads).values(link=i,
                                                       title=info[1],
                                                       price=info[2],
                                                       description=info[3])
                database.set_car(ins)

                for j in info[0]:
                    ins = database.insert(Images_cars).values(fk_link=i,
                                                              link=j)
                    database.set_image(ins, l)

                print(f"Машины и ее фотографии добавлены в базу данных {i}")
                time.sleep(3)

                page += 1
        except Exception as ex_:
            print('Bug', ex_)
            exit(0)

    print("Закончили парсинг всех странц")


def check_closed(URL):
    print("Зашли в функцию проверки закрытия объявляения\n", URL)

    browser = driver
    browser.get(URL)
    try:
        browser.find_element(By.CLASS_NAME, "closed-warning-content-_f4_B")
        print("Машина будет удалена")
        return True
    except:
        try:
            browser.find_element(By.CLASS_NAME, "page-title-count-wQ7pG")
            print("Машина будет удалена")
            return True
        except:
            print("Машина не будет удалена")
            return False


def drop_closed_ads(l):
    print("Зашли в функцию удалиния старых машин")

    s = select(database.Cars_ads.link)
    result = database.get_cars(s, l)
    for i in result:
        if check_closed(i[0]):
            del_photo = delete(database.Images_cars).where(
                Images_cars.fk_link == i[0])
            del_car = delete(database.Cars_ads).where(
                Cars_ads.link == i[0])

            database.set_image(del_photo, l)
            database.set_car(del_car, l)

            print(f"Машина с адресом: {i[0]} удалена")

        time.sleep(5)

    print("Старые машины удалены")
