import asyncio
import logging
import calendar
from datetime import datetime
import pytz

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardMarkup, KeyboardButton

from database.maindb import get_abbys_status, update_abbys_status, reg_user, get_all_id

token = ''
bot = Bot(token)
dp = Dispatcher()

button_1 = KeyboardButton(text='Запустить таймер')
button_2 = KeyboardButton(text='Закрыл бездну')

my_keyboard = ReplyKeyboardMarkup(
    keyboard=[[button_1], [button_2]],
    resize_keyboard=True
)

kb_without_start = ReplyKeyboardMarkup(
    keyboard=[[button_2]],
    resize_keyboard=True
)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - [%(levelname)s] - %(name)s - "
                           "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                    )


desired_timezone = pytz.timezone('Etc/GMT-4')


def days_in_month(year, month):
    return calendar.monthrange(year, month)[1]


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(text='Приветствую! Воспользуйтесь клавиатурой для запуска таймера',
                         reply_markup=my_keyboard)
    reg_user(message.from_user.id)


@dp.message(F.text == 'Запустить таймер')
async def timer(message: Message):
    await message.answer(text="Начато!", reply_markup=kb_without_start)
    while True:
        year = datetime.now(desired_timezone).year
        month = datetime.now(desired_timezone).month
        day = datetime.now(desired_timezone).day
        hour = datetime.now(desired_timezone).hour
        minute = datetime.now(desired_timezone).minute
        day_in_month = days_in_month(year, month)
        print(year, month, day, hour, minute)
        if get_abbys_status(message.from_user.id):
            if (day == 1 or day == 16) and hour == 23 and minute < 5:
                await message.answer(text='Бездна обновилась!')
            elif (day == day_in_month or day == 15) and hour == 23 and minute < 5:
                await message.answer(text='До обновления бездны осталось 7 часов!!!')
            elif (day == day_in_month - 1 or day == 14) and hour == 23 and minute < 5:
                await message.answer(text='До обновления бездны остался 1 день!!')
            elif (day == day_in_month - 2 or day == 13) and hour == 23 and minute < 5:
                await message.answer(text='До обновления бездны осталось 2 дня!')
            await asyncio.sleep(240)
        else:
            await asyncio.sleep(240)


@dp.message(F.text == 'Закрыл бездну')
async def done(message: Message):
    update_abbys_status(message.from_user.id, 0)
    await message.answer(text='Принято! Следующее оповещение будет послеобновления бездны.')
    while True:
        day = datetime.now(desired_timezone).day
        hour = datetime.now(desired_timezone).hour
        minute = datetime.now(desired_timezone).minute
        if not get_abbys_status(message.from_user.id):
            if (day == 1 or day == 16) and hour == 23 and minute < 5:
                await message.answer(text='Бездна обновилась!')
                update_abbys_status(message.from_user.id, 1)
                await asyncio.sleep(240)
        else:
            await asyncio.sleep(240)


async def start_bot():
    all_id = get_all_id()
    for user_id in all_id:
        user_id = user_id[0]
        await bot.send_message(user_id,
                               text='Bot started!',
                               reply_markup=my_keyboard)


async def main():
    dp.startup.register(start_bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
