from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import os

import pandas as pd
import numpy as np

TOKEN = '5398472247:AAFEpqmRrwHzdkNyDtamhtw8gP-9NywpSlU'

bot = Bot(token=TOKEN)

dp = Dispatcher(bot)

df = pd.read_csv('FAQ_Database.csv', sep=',', header=None)
data = df.values[1:]

data = np.array(data)
data = np.delete(data, [0, 1, 2, 3, 4, 5, 7, 8, 9], axis=1)


data = np.rot90(data, k=-1)
data[0] = np.array(list(map(lambda x: x.lower(),  data[0])))
data = np.rot90(data)




@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Привет!\nЭто поддержка Банка! \nПиши вопрос и мы постараемся тебе дать инструкцию "
                        "по использованию! ")

@dp.message_handler(content_types=types.ContentType.ANY)
async def echo(message: types.Message):
    messenge = (message.text).lower()
    if len(data[np.where(data[:,0] == messenge)]) != 0:
        for item in data[np.where(data[:,0] == messenge)][0]:
            if str(item) != 'nan' and str(item) != data[np.where(data[:,0] == messenge)][0][0]:
                await message.answer(item)

    else:
        # Всё, что не попадает под текст
        await message.answer("-")


if __name__ == '__main__':
    executor.start_polling(dp)
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,)
