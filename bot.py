from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import os
import pandas as pd
import numpy as np


TOKEN = '5398472247:AAFEpqmRrwHzdkNyDtamhtw8gP-9NywpSlU'


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

#
df = pd.read_csv('FAQ_Database.csv', sep=',', header=None) #читаем датасет
data = df.values[1:] #срез
data = np.array(data) #таблица в массив
data = np.delete(data, [0, 1, 2, 3, 4, 5, 7, 8, 9], axis=1) #удаляем ненужные данные
data = np.rot90(data, k=-1)
data[0] = np.array(list(map(lambda x: x.lower(),  data[0]))) #
data = np.rot90(data)

@dp.message_handler(commands=['start']) #функция старта и описания бота
async def process_start_command(message: types.Message):
    await message.reply("Привет!🤖\nЭто поддержка Банка «Открытие» 🚀 \n Пиши вопрос или выбирай из списка, "
                        "мы постараемся тебе дать инструкцию "
                        "по использованию!🤩 "
                        "\n Вот тебе FAQ, который тебе поможет разобраться с правильной постановкой"
                        " вопроса для бота:"
                        "\n https://docs.google.com/document/d/1CaDX8YLVpDlZWWkpmcbaNQHu8AwieoEMdfdiMdcSt0s/edit"
                        "\n 🥳И пример вопросов из FAQ 🥳:"
                        "\n - Как настроить автоплатеж по расписанию после совершения операции"
                        "\n - Как удалить автоплатеж"
                        "\n - Как найти ближайший офис банка"
                        "\n - Как узнать график работы кассы и депозитария"
                        "\n - Как узнать график работы кассы и депозитария"
                        "\n - Как записаться в офис")


@dp.message_handler(content_types=types.ContentType.ANY) #основная функция бота
async def echo(message: types.Message):
    messenge = (message.text).lower()
    if len(data[np.where(data[:,0] == messenge)]) != 0:
        for item in data[np.where(data[:,0] == messenge)][0]:
            if str(item) != 'nan' and str(item) != data[np.where(data[:,0] == messenge)][0][0]:
                await message.answer(item)

    else:
        # Всё, что не попадает под текст
        await message.answer("Сформулируй свой вопрос через FAQ!🤩"
                             "\n https://docs.google.com/document/d/1CaDX8YLVpDlZWWkpmcbaNQHu8AwieoEMdfdiMdcSt0s/edit ")


if __name__ == '__main__':
    executor.start_polling(dp)
