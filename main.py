from aiogram import Bot,Dispatcher,types,executor
from aiogram.dispatcher.filters.state import State,StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters import Text
from pyqiwip2p import QiwiP2P


import config
from markup import *
from modify import *
from request import *
from imagemaker import *
from db import *
from checker import *

bot = Bot(token=config.TOKEN, parse_mode="HTML")
storage = MemoryStorage()
dp = Dispatcher(bot,storage=storage)

p2p = QiwiP2P(auth_key=config.PRIVATE_KEY)

class State(StatesGroup):
    get_number = State()

class Data():
    bus = int
    bus_name = str
    bus_number = str
    time = str
    start_station = str
    stop_station = str

def get_message_answer():
    return ('Сгенерировать чек?\n'
             f'Автобус №{Data.bus}\n'
             f'Номерной знак: {Data.bus_number}\n'
             f'Время сейчас: {Data.time}\n'
             f'Начальная остановка: {Data.start_station}\n'
             f'Конечная остановка: {Data.stop_station}\n'
             f'Название машрута: {Data.bus_name}')

@dp.message_handler(commands = ['alert'],state=None)
async def start(message: types.Message):
    if (flag_admin(message.from_user.id)):
        for id in get_active_users_list():
            try:
                await bot.send_message(int(id),message.text[message.text.find(' '):])
            except:
                await bot.send_message(get_admin_id(),f'Отправка пользователю {get_user_info(id)} невозможна')
                deactivate_user(id)
    else:
        await bot.send_message(message.from_user.id,'Данная команда недоступна для вас!')

@dp.message_handler(commands = ['start'],state=None)
async def start(message: types.Message):
    create_user(message.from_user.id,f'@{message.from_user.username}',f'{message.from_user.first_name} {message.from_user.last_name}')
    await message.answer('Добро пожаловать. Я бот, который сделает вам настоящий чек об оплате автобуса в ВОЛГА-Тверь',reply_markup=keyboard_main)

@dp.message_handler(Text(equals='Сгенерировать чек'))
async def generate_check(message: types.Message,state: FSMContext):
    await state.finish()
    inline_kb_bus = create_bus_inline(get_bus_numbers())
    await message.answer('Выберите номер автобуса',reply_markup=inline_kb_bus)

@dp.message_handler(Text(equals='Помощь'))
async def generate_check(message: types.Message,state: FSMContext):
    await state.finish()
    await bot.send_message(message.from_user.id,'<a href="https://t.me/petya_petrov">Обращаться по любым вопросам</a>',parse_mode='html')

@dp.message_handler(Text(equals='Подписка'))
async def generate_check(message: types.Message,state: FSMContext):
    await state.finish()
    #Работаю с датами
    await message.answer(f'Ваш аккаунт:\n{get_user_info(message.from_user.id)}')
    if not get_sub(message.from_user.id):
        bill = p2p.bill(amount=config.SUB_PRICE, lifetime=15, comment=str(message.from_user.id))
        await message.answer(f'У вас нет активной подписки.\n'
                             f'Для покупки подписки отправьте {config.SUB_PRICE} рублей\n'
                             f'На счет QIWI +79011223917\n'
                             f'Указав комментарий к оплате {str(message.from_user.id)}\n'
                             f'Или просто нажмите кнопку "Купить"\n'
                             f'После перевода денег нажмите "Проверить оплату"\n'
                             f'Внимание!\n'
                             f'1. Не забудьте указать комментарий к переводу {str(message.from_user.id)}\n'
                             f'2. Не нажимайте кнопку "Подписка", если перевели деньги и не нажали "Проверить оплату".\n'
                             f'3. Переводите {config.SUB_PRICE} рублей или больше.', reply_markup=create_buy_inline(url=bill.pay_url,bill=bill.bill_id), parse_mode='html')

@dp.message_handler(state=State.get_number)
async def get_bus_number(message: types.Message,state: FSMContext):
    if message.text == 'Сгенерировать чек':
        await state.finish()
    else:
        Data.bus_number = message.text.upper().replace('РС','СР')
        inline_kb_start = create_start_station_inline(get_bus_stations(str(Data.bus)))
        await bot.send_message(message.from_user.id,'Выберите начальную остановку',reply_markup=inline_kb_start)
        await state.finish()

@dp.callback_query_handler(text_contains="check_")
async def check(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)

    bill = str(call.data.replace('check_',''))
    print(bill)

    if str(p2p.check(bill_id=bill).status) == "PAID":   #Оплата прошла
        if config.SUB_PRICE <= int(str(p2p.check(bill_id=bill).amount).split('.')[0]): #Оплата прошла и на нужную сумма
            sub_activate(call.from_user.id)
            await bot.send_message(call.from_user.id, f"Оплата на {p2p.check(bill_id=bill).amount} прошла успешно!\n"
                                                        f"Ативирована подписка на месяц (до {get_date_deactivate(call.from_user.id)})")

        else:
            await bot.send_message(call.from_user.id,f"Вы оплатили {p2p.check(bill_id=bill).amount} рублей, а требовалось {config.SUB_PRICE}!")
    else:
        await bot.send_message(call.from_user.id, "Вы не оплатили счет!",reply_markup=create_buy_inline(False,bill=bill))

@dp.callback_query_handler(text_contains="bus_")
async def check(call: types.CallbackQuery):
    Data.bus = int(str(call.data).replace('bus_', ''))
    Data.time = get_time()
    Data.bus_name = get_bus_name(Data.bus)
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, 'Введите номерной знак автобуса (Пример: н 132 ср)')
    await State.get_number.set()

@dp.callback_query_handler(text_contains="start_")
async def check(call: types.CallbackQuery):
    Data.start_station = get_bus_stations(Data.bus)[int(str(call.data).replace('start_', ''))]
    inline_kb_stop = create_stop_station_inline(get_bus_stations(str(Data.bus)))
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, 'Выберите конечную остановку', reply_markup=inline_kb_stop)

@dp.callback_query_handler(text_contains="stop_")
async def check(call: types.CallbackQuery):
    Data.stop_station = get_bus_stations(Data.bus)[int(str(call.data).replace('stop_', ''))]
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, get_message_answer(), reply_markup=markup_true_false)

@dp.callback_query_handler(text_contains="buttonTrue")
async def check(call: types.CallbackQuery):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    if (get_sub(call.from_user.id)):
        await bot.send_message(call.from_user.id, "Ожидайте генерирую чек...", reply_markup=keyboard_main)
        url_qr = get_request(Data.bus,
                             Data.bus_name,
                             Data.bus_number,
                             Data.time,
                             Data.start_station,
                             Data.stop_station)
        path_to_image = create_image(Data.bus, Data.bus_number, Data.start_station, Data.stop_station, url_qr)
        await bot.send_document(call.from_user.id, document=open(path_to_image, 'rb'))
        os.remove(path_to_image)
    else:
        await bot.send_message(call.from_user.id, "Я не могу сгенерировать чек. У вас нет подписки!",
                               reply_markup=keyboard_main)

@dp.callback_query_handler(text_contains="buttonFalse")
async def check(call: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(call.from_user.id, call.message.message_id)
    await bot.send_message(call.from_user.id, 'Удаляю информацию, давайте попробуем заново', reply_markup=keyboard_main)
    await state.finish()

@dp.message_handler(content_types=['text'],state=None)
async def answer(message: types.Message, state:FSMContext):
    await message.answer('Я вас не понимаю', reply_markup=keyboard_main)

if __name__ == '__main__':
    main_core_check()
    try:
        executor.start_polling(dp, skip_updates=True)
    except Exception as ex:
        print(ex)
