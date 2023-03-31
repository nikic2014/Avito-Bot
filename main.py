import datetime
import multiprocessing
import time

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    InputMedia
from aiogram.utils.callback_data import CallbackData
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from multiprocessing import Process, Manager

from aiogram.utils.exceptions import BadRequest
from sqlalchemy import select

import GUI
import config
import const
from config import TOKEN_BOT
from parsers import parser_selenium
import database
from parsers.parser_selenium import drop_closed_ads
# import MyLogging
from MyLogging import bot_loger


storage = MemoryStorage()
bot = Bot(token=TOKEN_BOT,
          parse_mode=types.ParseMode.HTML
          )
dp = Dispatcher(bot, storage=storage)

cars_list = {}
photo_list = {}


def BOT(cars_list_up_300,
        cars_list_up_1000,
        cars_list_up_INF,
        lock):
    bot_loger.info(f"Зашли в функцию BOT")

    try:
        @dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            await message.answer("<em>Добро пожаловать!\n"
                                 "Данный бот позволяет просматривать объявления"
                                 " на авито, в выбранной вами категории "
                                 "в Саратове.</em>",
                                 reply_markup=GUI.main_kb,
                                 parse_mode="HTML")
            # bot_loger.info("Стартовое сообщение успешно отправлено")

        @dp.message_handler(text='Квартиры')
        async def apartment(message: types.Message):
            await message.answer("Выберите количество комнат",
                                 reply_markup=GUI.apartment_kb)
            # bot_loger.info("Кнопка квартиры успешно обработана")

        @dp.message_handler(text='Машины')
        async def car(message: types.Message):
            await message.answer("Выберите ценовой сегмент",
                                 reply_markup=GUI.car_kb)

        @dp.message_handler(text='Назад')
        async def back_in_main(message: types.Message):
            await message.answer("Вы в главном меню", reply_markup=GUI.main_kb)

        @dp.message_handler(text='Связь с разработчиком')
        async def contact_developer(message: types.Message):
            await message.answer('@Sad_prod')

        cars_callback_data = CallbackData('car', 'pages')

        def get_car_keyboard(page_car: int = 0, page_photo: int = 0):
            keyboard = InlineKeyboardMarkup(row_width=2)
            next_photo_button = InlineKeyboardButton("Photo ▶",
                                                     callback_data=cars_callback_data.new(
                                                         pages=[page_car,
                                                                page_photo + 1]))
            previous_photo_button = InlineKeyboardButton("◀ Photo",
                                                         callback_data=cars_callback_data.new(
                                                             pages=[page_car,
                                                                    page_photo - 1]))
            next_car_button = InlineKeyboardButton("Car ▶",
                                                   callback_data=cars_callback_data.new(
                                                       pages=[page_car + 1,
                                                              0]))
            previous_car_button = InlineKeyboardButton("◀ Car",
                                                       callback_data=cars_callback_data.new(
                                                           pages=[page_car - 1,
                                                                  0]))
            keyboard.add(previous_photo_button, next_photo_button)
            keyboard.add(previous_car_button, next_car_button)

            return keyboard

        @dp.message_handler(text='До 300 тыс')
        async def cars_up_to_300(message: types.Message):
            global cars_list, cars_list_up_300
            cars_list = cars_list_up_300
            print(len(cars_list))
            bot_loger.info(f"Длина 1 списка машин:"
                           f"{len(cars_list)}")
            await cars_menu(message)

        @dp.message_handler(text='От 300 тыс до 1 млн')
        async def cars_up_to_milion(message: types.Message):
            global cars_list, cars_list_up_1000
            cars_list = cars_list_up_1000
            print(len(cars_list))
            bot_loger.info(f"Длина 2 списка машин:"
                           f"{len(cars_list)}")
            await cars_menu(message)

        @dp.message_handler(text='Больше 1 млн')
        async def cars_up_to_milion(message: types.Message):
            global cars_list, cars_list_up_INF
            cars_list = cars_list_up_INF
            print(len(cars_list))
            bot_loger.info(f"Длина 3 списка машин:"
                           f"{len(cars_list)}")
            await cars_menu(message)

        async def cars_menu(message: types.Message):
            global photo_list, cars_list


            caption = f"Автомобиль: {cars_list[0][1]}\n" \
                      f"Цена: {cars_list[0][2]}\n" \
                      f"Описание:\n{cars_list[0][3]}"
            keyboard = get_car_keyboard()  # Page: 0
            print(caption)

            s = select(database.Images_cars.link).where(
                database.Images_cars.fk_link == cars_list[0][0])
            result = database.get_images(s, lock)
            photo_list = result

            await bot.send_photo(
                chat_id=message.chat.id,
                photo=cars_list[0][0],
                caption=caption,
                parse_mode="HTML",
                reply_markup=keyboard
            )

        @dp.callback_query_handler(cars_callback_data.filter())
        async def cars_page_handler(callback: types.CallbackQuery,
                                    callback_data: dict):
            try:
                pages = callback_data.get("pages")
                page_car = int(pages[1:].split(',')[0])
                page_photo = int(pages[:-1].split(',')[1])

                if (page_photo < 0):
                    await callback.answer("Вы в самом начале")
                    return

                global photo_list

                if page_photo == 0:
                    s = select(database.Images_cars.link).where(
                        database.Images_cars.fk_link == cars_list[page_car][0])
                    result = database.get_images(s, lock)
                    photo_list = result

                caption = f"Автомобиль: {cars_list[page_car][1]}\n" \
                          f"Цена: {cars_list[page_car][2]}\n" \
                          f"Описание:\n{cars_list[page_car][3]}\n" \
                          f"Cсылка: \n {cars_list[page_car][0]}"
                if len(caption) > 1024:
                    caption = \
                    f"Автомобиль: {cars_list[page_car][1]}\n" \
                    f"Цена: {cars_list[page_car][2]}\n" \
                    f"Описание: К сожалению описание слишком длинное, " \
                                f"вы можете ознакомиться с ним по ссылке на машину. \n" \
                    f"Cсылка: \n {cars_list[page_car][0]}"

                caption = caption.replace("<br>", '')
                keyboard = get_car_keyboard(page_car=page_car,
                                            page_photo=page_photo)  # Page: 0
                photo = InputMedia(type="photo",
                                   media=photo_list[page_photo][0],
                                   caption=caption,
                                   parse_mode="HTML"
                                   )

                await callback.message.edit_media(photo, keyboard)
            except IndexError:
                await callback.answer("Вы дошли до конца")
            except BadRequest as exept:
                bot_loger.error(exept.args)

    except Exception as ex_:
        bot_loger.error("Error while working with BOT:", ex_, traceback=True)

    executor.start_polling(dp, skip_updates='true')
    bot_loger.info("Бот успешно запущен")

def write_lists(l1, l2, l3, lock):
    bot_loger.info("Зашли в функцию write_lists")

    s = select(database.Cars_ads).where(database.Cars_ads.price <= 300000)
    result = database.get_cars(s, lock)
    for i in result:
        l1.append(i)

    s = select(database.Cars_ads).where(
        database.Cars_ads.price.between(300000, 1000000))
    result = database.get_cars(s, lock)
    for i in result:
        l2.append(i)

    s = select(database.Cars_ads).where(database.Cars_ads.price > 1000000)
    result = database.get_cars(s, lock)
    for i in result:
        l3.append(i)

    bot_loger.info("Зашли записали информацию о всех машинах")
    bot_loger.info(f"Первый список машин {l1}")
    bot_loger.info(f"Второй список машин {l2}")
    bot_loger.info(f"Третий список машин {l3}")


def call_parse(l1, l2, l3, lock):
    while True:
        bot_loger.info("Запуск фукнции call_parse")

        write_lists(l1, l2, l3, lock)

        drop_closed_ads(lock)
        parser_selenium.test_parse("https://www.avito.ru/saratov/"
                                   "avtomobili?cd=1&radius=0&searchRadius=0",
                                   lock)

        bot_loger.info("Прошла одна итерация call_parse")


if __name__ == '__main__':
    with Manager() as manager:
        bot_loger.info("Запуск функции main")

        lock = multiprocessing.Lock()

        cars_list_up_300 = manager.list()
        cars_list_up_1000 = manager.list()
        cars_list_up_INF = manager.list()

        p1 = Process(target=BOT, args=(cars_list_up_300,
                                       cars_list_up_1000,
                                       cars_list_up_INF,
                                       lock))
        p2 = Process(target=call_parse, args=(cars_list_up_300,
                                              cars_list_up_1000,
                                              cars_list_up_INF,
                                              lock))
        p1.start()
        p2.start()
        p1.join()
        p2.join()
    pass
