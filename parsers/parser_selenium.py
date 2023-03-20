import time

from selenium import webdriver
from selenium.webdriver.common.by import By
# from parsers.parser_beautiful_soup import parse_current_car
import sqlalchemy as db
from sqlalchemy import select
from sqlalchemy.orm import Session

import database
from database import Cars_ads, Images_cars, engine

"""
def parse_car():
    browser = webdriver.Chrome()

    URL = "https://www.avito.ru/saratov/avtomobili?cd=1&radius=50&searchRadius=50"
    browser.get(URL)

    step1 = browser.find_element(By.CLASS_NAME, "index-content-_KxNP")
    step2 = step1.find_element(By.CLASS_NAME, "index-root-KVurS")
    step3 = step2.find_element(By.CLASS_NAME, "items-items-kAJAg")

    cars = step3.find_elements(By.TAG_NAME, "div")
    links_car = []

    for i in cars:
        try:
            links_car.append(i.find_element(By.CLASS_NAME,
                                            "iva-item-content-rejJg").find_element(
                By.TAG_NAME, "a").get_attribute("href"))
        except Exception as ex:
            #print(ex)
            pass
    print(links_car)

    browser.quit()

    obj_car = []

    for i in links_car:
        current_car = parse_current_car(i)
        obj_car.append(current_car)
        print(current_car)

    print(obj_car)



    # links = browser.find_elements(By.CLASS_NAME, "title-info-title-text")
    # print(links[0].get_attribute("innerHTML"))
"""


def parse_info(URL):
    browser = webdriver.Chrome()
    browser.get(URL)

    img_array = []

    title = browser.find_element(By.CLASS_NAME,
                                 "title-info-title-text").get_attribute(
        "innerHTML")
    print(title)

    description = None
    try:
        description = browser.find_element(By.CLASS_NAME,
                                           "style-item-description"
                                           "-text-mc3G6").find_element(
            By.TAG_NAME, "p").get_attribute("innerHTML")
    except:
        description = browser.find_element(By.CLASS_NAME,
                                           "style-item-description"
                                           "-html-qCwUL").find_element(
            By.TAG_NAME, "p").get_attribute("innerHTML")
    print(description)

    price = browser.find_element(By.CLASS_NAME,
                                 "style-price-value-main-TIg6u").find_element(
        By.TAG_NAME, "span").get_attribute("content")
    print(price)

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


def test_parse(URL):
    page = 1
    while True:
        try:
            URL = str(URL).replace("p=", f"p={page}")

            browser = webdriver.Chrome()
            browser.get(URL)
            time.sleep(5)

            links = []
            cars = browser.find_elements(By.CLASS_NAME,
                                         "iva-item-titleStep-pdebR")
            for i in cars:
                link = i.find_element(By.TAG_NAME, "a").get_attribute("href")
                with Session(engine) as session:
                    s = select(Cars_ads).where(Cars_ads.link == link)
                    result = session.execute(s).fetchone()

                if result is None:
                    links.append(link)

            browser.quit()

            for i in links:
                info = parse_info(i)
                if info == []:
                    print("Bug fixed", i)
                    continue

                ins = database.insert(Cars_ads).values(link=i,
                                                       title=info[1],
                                                       price=info[2],
                                                       description=info[3])
                compiled = ins.compile()
                result = database.conaction.execute(ins)
                database.conaction.commit()

                for j in info[0]:
                    ins = database.insert(Images_cars).values(fk_link=i,
                                                              link=j)
                    compiled = ins.compile()
                    result = database.conaction.execute(ins)
                    database.conaction.commit()

                print(info)
                time.sleep(3)

                page += 1
        except Exception as ex_:
            print('Bug', ex_)
            exit(0)

