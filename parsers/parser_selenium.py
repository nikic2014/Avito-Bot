import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from parsers.parser_beautiful_soup import parse_current_car

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

# parse_car()

def parse_image(URL):
    browser = webdriver.Chrome()
    browser.get(URL)

    img_array = []

    # if (browser.find_element(By.CLASS_NAME, "closed-warning-linkText-bXEpX"))

    while 1:
        try:
            class_image = browser.find_element(By.CLASS_NAME,
                                               "image-frame-wrapper-_NvbY")
            tag_image = class_image.find_element(By.TAG_NAME, "img")
            link_image = tag_image.get_attribute("src")
            if link_image in img_array:
                break
            img_array.append(link_image)
            print(link_image)
        except:
            break

        try:
            btn = browser.find_elements(By.CLASS_NAME, "image-frame-controlButton-_vPNK")
            btn[1].click()
            time.sleep(0.5)
        except:
            return []
    return img_array


def test_parse(URL):
    browser = webdriver.Chrome()

    browser.get(URL)
    links = []
    cars = browser.find_elements(By.CLASS_NAME, "iva-item-titleStep-pdebR")
    for i in cars:
        link = i.find_element(By.TAG_NAME, "a").get_attribute("href")
        links.append(link)

    browser.quit()

    for i in links:
        images = parse_image(i)
        if images == []:
            print("Bug fixed", i)
            continue
        time.sleep(3)


#test_parse("https://www.avito.ru/saratov/avtomobili?cd=1&radius=50&searchRadius=50")