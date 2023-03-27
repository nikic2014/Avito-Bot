from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, \
    InputMedia
from aiogram.utils.callback_data import CallbackData
from aiogram_calendar import simple_cal_callback, SimpleCalendar, \
    dialog_cal_callback, DialogCalendar
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
# import psycopg2
import datetime
import asyncio
import threading
import time
from multiprocessing import Process

from sqlalchemy import select

import const
import GUI
from config import TOKEN_BOT
from parsers import parser_selenium
import database

storage = MemoryStorage()
bot = Bot(token=TOKEN_BOT,
          parse_mode=types.ParseMode.HTML
          )
dp = Dispatcher(bot, storage=storage)

# conaction = psycopg2.connect(
#     host=host,
#     user=user,
#     password=password,
#     database=db_name
# )

cars_list = {}
photo_list = {}


def BOT():
    try:
        @dp.message_handler(commands=['start'])
        async def start(message: types.Message):
            await message.answer("<em>Добро пожаловать!\n"
                                 "Данный бот позволяет просматривать объявления"
                                 " на авито, в выбранной вами категории "
                                 "в Саратове.</em>",
                                 reply_markup=GUI.main_kb,
                                 parse_mode="HTML")

        @dp.message_handler(text='Квартиры')
        async def apartment(message: types.Message):
            await message.answer("Выберите количество комнат",
                                 reply_markup=GUI.apartment_kb)

        @dp.message_handler(text='Машины')
        async def car(message: types.Message):
            await message.answer("Выберите ценовой сегмент",
                                 reply_markup=GUI.car_kb)

        @dp.message_handler(text='До 300 тыс')
        async def car(message: types.Message):
            await message.answer("Выберите ценовой сегмент",
                                 reply_markup=GUI.inline_car_kb)

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

        @dp.message_handler(commands=["test"])
        async def testing(message: types.Message):
            global photo_list

            caption = f"Автомобиль: {cars_list[0][1]}\n" \
                      f"Цена: {cars_list[0][2]}\n" \
                      f"Описание:\n{cars_list[0][3]}"
            keyboard = get_car_keyboard()  # Page: 0

            s = select(database.Images_cars.link).where(
                database.Images_cars.fk_link == cars_list[0][0])
            result = database.conaction.execute(s).fetchall()
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
                    result = database.conaction.execute(s).fetchall()
                    photo_list = result

                caption = f"Автомобиль: {cars_list[page_car][1]}\n" \
                          f"Цена: {cars_list[page_car][2]}\n" \
                          f"Описание:\n{cars_list[page_car][3]}\n" \
                          f"Cсылка: \n {cars_list[page_car][0]}"
                keyboard = get_car_keyboard(page_car=page_car,
                                            page_photo = page_photo)  # Page: 0
                photo = InputMedia(type="photo",
                                   media=photo_list[page_photo][0],
                                   caption=caption)

                await callback.message.edit_media(photo, keyboard)
            except IndexError:
                await callback.answer("Вы дошли до конца")


    except Exception as ex_:
        print("Error while working with Bot:", ex_)
    except:
        print('Exept in main.py')

    executor.start_polling(dp, skip_updates='true')


def call_parse():
    while True:
        parser_selenium.test_parse("https://www.avito.ru/saratov/avtomobili/"
                                   "do-300000-rubley-ASgCAgECAUXGmgwWeyJmcm9tIjowLCJ0byI6MzAwMDAwfQ?cd=1&p=&radius=50&searchRadius=50")
        # asyncio.sleep(79200) ### Парсинг каждые 22 часа
        # new_kd();


if __name__ == '__main__':
    # p1 = Process(target=BOT)
    # p1.start()
    # p2 = Process(target=call_parse())
    # p2.start()
    # p1.join()
    # p2.join()
    # call_parse()

    s = select(database.Cars_ads).where(database.Cars_ads.price < 2000000)
    result = database.conaction.execute(s).fetchall()
    cars_list = result

    print(result)
    BOT()
    pass
