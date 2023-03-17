from aiogram import Bot, Dispatcher, executor, types
from aiogram_calendar import simple_cal_callback, SimpleCalendar, \
    dialog_cal_callback, DialogCalendar
from aiogram.dispatcher.filters import Text
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
import psycopg2
import datetime
import asyncio
import threading
import time
from multiprocessing import Process

import const
import GUI
from config import host, user, password, db_name, TOKEN_BOT
from parsers import parser_selenium

storage = MemoryStorage()
bot = Bot(token=TOKEN_BOT,
          parse_mode=types.ParseMode.HTML
          )
dp = Dispatcher(bot, storage=storage)

conaction = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

print("Соединение открыто")


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
            await bot.send_photo(message.chat.id,
                                 "https://10.img.avito.st/image/1/1.mzKEXLa3N9uk_ltVm3qWWjP_N9E6aTS3Mv8.hQrExpzBoBTeGM3wQ-qCwTO8oObnvB3_7TERO_0_r2w")
            await message.answer("Выберите ценовой сегмент",
                                 reply_markup=GUI.car_kb)

        @dp.message_handler(text='Назад')
        async def back_in_main(message: types.Message):
            await message.answer("Вы в главном меню", reply_markup=GUI.main_kb)

        @dp.message_handler(text='Связь с разработчиком')
        async def contact_developer(message: types.Message):
            await message.answer('@Sad_prod')


    except Exception as ex_:
        print("Error while working with PostgreSQL:", ex_)
    except:
        print('Exept in main.py')

    executor.start_polling(dp, skip_updates='true')

def call_parse():
    while True:
        parser_selenium.test_parse(
            "https://www.avito.ru/saratov/avtomobili?cd=1&p=&radius=50&searchRadius=50")
        parser_selenium.test_parse("https://www.avito.ru/saratov/avtomobili/do-300000-rubley-ASgCAgECAUXGmgwWeyJmcm9tIjowLCJ0byI6MzAwMDAwfQ?cd=1&p=&radius=50&searchRadius=50")
        asyncio.sleep(79200) ### Парсинг каждые 22 часа

if __name__ == '__main__':
    # p1 = Process(target=BOT)
    # p1.start()
    # p2 = Process(target=call_parse())
    # p2.start()
    # p1.join()
    # p2.join()
    call_parse()
