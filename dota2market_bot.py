import time
import json
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.markdown import hbold, hlink, hide_link
from dotenv import find_dotenv, load_dotenv

from main import collect_data

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start_handler(message: types.Message):
    start_button = KeyboardButton('Запуск бота')
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(start_button)

    await message.answer('Запустите бота!\n', reply_markup=keyboard)


@dp.message_handler(Text(equals='Запуск бота'))
async def get_items_handler(message: types.Message):
    await message.answer('Пожалуйста, подождите...')

    total_count = collect_data()

    if total_count == 0:
        await message.answer('К сожалению, предметов с данными фильтрами на данный момент нет!')
        return

    with open('result.json', 'r') as file:
        data = json.load(file)

    for index, item in enumerate(data):
        card = f'{hide_link(data[item]["image_url"])}\n' \
               f'{hlink(data[item]["full_name"].replace("%20", " "), data[item]["url"])}\n' \
               f'{hbold("Цена: ")}{data[item]["price"]} руб.'

        if index % 15 == 0:
            time.sleep(3)

        await message.answer(card)


async def on_startup(dp):
    print('Бот запущен!')


if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
