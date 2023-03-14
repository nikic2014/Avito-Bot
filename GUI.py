from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
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

    # создание inline меню для car
    # time_kb = InlineKeyboardMarkup(row_width=1)
    # day_button = InlineKeyboardButton(const.day, callback_data=const.day)
    # week_button = InlineKeyboardButton(const.week, callback_data=const.week)
    # month_button = InlineKeyboardButton(const.month, callback_data=const.month)
    # year_button = InlineKeyboardButton(const.year, callback_data=const.year)
    # time_kb.add(day_button)
    # time_kb.add(week_button)
    # time_kb.add(month_button)
    # time_kb.add(year_button)

except:
    print('Exept in GUI')
