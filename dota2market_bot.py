import time
import json
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink, hide_link
from dotenv import find_dotenv, load_dotenv

from main import collect_data

load_dotenv(find_dotenv())

bot = Bot(token=os.getenv('TOKEN'), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    start_buttons = ['Запуск бота']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)

    await message.answer('Запустите бота!\n', reply_markup=keyboard)


@dp.message_handler(Text(equals='Запуск бота'))
async def get_items(message: types.Message):
    await message.answer('Please waiting...')

    total_count = collect_data()

    if total_count != 0:

        with open('result.json', 'r') as file:
            data = json.load(file)

        for index, item in enumerate(data):
            card = f'{hide_link(data.get(item).get("image_url"))}\n' \
                   f'{hlink(data.get(item).get("full_name").replace("%20", " "), data.get(item).get("url"))}\n' \
                   f'{hbold("Цена: ")}{data.get(item).get("price")} руб.'

            if index % 10 == 0:
                time.sleep(3)

            await message.answer(card)
    else:
        await message.answer('К сожалению предметов с данными фильтрами на данный момент нет!')


def main():
    print('Bot Online!')
    executor.start_polling(dp)


if __name__ == '__main__':
    main()
