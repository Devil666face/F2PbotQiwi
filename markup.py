import aiogram
from aiogram import types
from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton
from aiogram.types.message import ContentTypes
from aiogram.types.message import ContentType

main_buttons = ['Сгенерировать чек','Подписка','Помощь']
keyboard_main = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard_main.add(*main_buttons)

markup_true_false = InlineKeyboardMarkup(row_width=2)
item_true = InlineKeyboardButton(text = 'Ок',callback_data = 'buttonTrue')
item_false = InlineKeyboardButton(text = 'Отменить',callback_data = 'buttonFalse')
markup_true_false.add(item_true,item_false)

def create_buy_inline(isUrl=True, url="", bill=""):
    markup_buy_sub = InlineKeyboardMarkup(row_width=1)
    if isUrl:
        item_buy = InlineKeyboardMarkup(text='Купить', url=url)
        markup_buy_sub.add(item_buy)
    item_check = InlineKeyboardMarkup(text='Проверить оплату', callback_data=f'check_{bill}')
    markup_buy_sub.add(item_check)
    return markup_buy_sub

def create_bus_inline(bus_number_list):
    inline_kb = types.InlineKeyboardMarkup()
    for bus_number in bus_number_list:
        inline_kb.add(types.InlineKeyboardButton(text=f'{bus_number}', callback_data=f'bus_{bus_number}'))
    return inline_kb

def create_start_station_inline(bus_station_list):
    inline_kb = types.InlineKeyboardMarkup()
    for i in range (0,len(bus_station_list)):
        inline_kb.add(types.InlineKeyboardButton(text=f'{bus_station_list[i]}', callback_data=f'start_{i}'))
    return inline_kb

def create_stop_station_inline(bus_station_list):
    inline_kb = types.InlineKeyboardMarkup()
    for i in range(0, len(bus_station_list)):
        inline_kb.add(types.InlineKeyboardButton(text=f'{bus_station_list[i]}', callback_data=f'stop_{i}'))
    return inline_kb
