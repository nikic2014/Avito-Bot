from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

import const

try:
    # создание главного меню
    main_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    button_apartment = KeyboardButton('Квартиры')
    button_car = KeyboardButton('Машины')
    button_feedback = KeyboardButton('Связь с разработчиком')
    main_kb.add(button_apartment)
    main_kb.add(button_car)
    main_kb.add(button_feedback)

    # ссоздание Reply меню для apartment
    apartment_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    one_room = KeyboardButton('Однокомнатные квартиры')
    two_room = KeyboardButton('Двухкомнатные квартиры')
    three_room = KeyboardButton('Трехкомнатные квартиры')
    button_back = KeyboardButton('Назад')
    apartment_kb.add(one_room)
    apartment_kb.add(two_room)
    apartment_kb.add(three_room)
    apartment_kb.add(button_back)

    # создание Reply меню для car
    car_kb = ReplyKeyboardMarkup(resize_keyboard=True)
    low_price = KeyboardButton('До 300 тыс')
    normal_price = KeyboardButton('От 300 тыс до 1 млн')
    high_price = KeyboardButton('Больше 1 млн')
    button_back = KeyboardButton('Назад')
    car_kb.add(low_price)
    car_kb.add(normal_price)
    car_kb.add(high_price)
    car_kb.add(button_back)

    # пример inline меню для car
    # inline_car_kb = InlineKeyboardMarkup(row_width=2)
    # next_photo_button = InlineKeyboardButton("Photo ▶", callback_data="->")
    # previous_photo_button = InlineKeyboardButton("◀ Photo", callback_data="<-")
    # next_car_button = InlineKeyboardButton("Car ▶", callback_data="->")
    # previous_car_button = InlineKeyboardButton("◀ Car", callback_data="<-")
    # inline_car_kb.add(previous_photo_button, next_photo_button)
    # inline_car_kb.add(previous_car_button, next_car_button)

except:
    print('Exept in GUI')
