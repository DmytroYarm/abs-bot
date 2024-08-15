import logging
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile

from autonova.autonova_main import AutonovaMain
from emex.emex_main import EmexMain

import os
from datetime import datetime
from dotenv import load_dotenv
import asyncio

AUTHORIZED_USERS = [573801983, 5255367200]

schedule_flags = {
    'emex': False,
    'autonova': False
}

emex_task = None
autonova_task = None

logging.basicConfig(level=logging.INFO)

load_dotenv()
bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher(bot)


async def toggle_schedule(callback_query: types.CallbackQuery, key: str):
    global emex_task, autonova_task

    schedule_flags[key] = not schedule_flags[key]

    if schedule_flags[key]:
        await callback_query.message.answer(f"Розклад увімкнено")

        if key == 'emex':
            emex_task = asyncio.create_task(run_emex_schedule(callback_query.message))
        elif key == 'autonova':
            autonova_task = asyncio.create_task(run_autonova_schedule(callback_query.message))
    else:
        await callback_query.message.answer(f"Розклад вимкнено")

        if key == 'emex' and emex_task:
            emex_task.cancel()
            emex_task = None
        elif key == 'autonova' and autonova_task:
            autonova_task.cancel()
            autonova_task = None


async def run_emex_schedule(message):
    try:
        while True:
            current_time = datetime.now().time()
            if current_time.hour == 0 and current_time.minute == 55:
                await message.answer(EmexMain().main(), parse_mode='HTML')
            await asyncio.sleep(60)
    except asyncio.CancelledError:
        pass


async def run_autonova_schedule(message):
    try:
        while True:
            current_time = datetime.now().time()
            if current_time.hour == 23 and current_time.minute == 30:
                await message.answer(AutonovaMain().main(), parse_mode='HTML')
            await asyncio.sleep(60)
    except asyncio.CancelledError:
        pass


def get_main_menu_keyboard(user_id):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(types.KeyboardButton("⚙️EMEX"), types.KeyboardButton("⚙️AUTONOVA"))
    keyboard.add(types.KeyboardButton("📖Документація ABS-bot"))
    # if user_id in AUTHORIZED_USERS:
    #     keyboard.add(types.KeyboardButton("Go Back"))
    return keyboard


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    keyboard = get_main_menu_keyboard(message.from_user.id)
    await message.answer("Оберіть платформу:", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "⚙️EMEX")
async def show_emex_options(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Завантажити прайси", callback_data="emex_load_prices"))
    keyboard.add(InlineKeyboardButton("Завантаження за розкладом", callback_data="emex_schedule"))
    keyboard.add(InlineKeyboardButton("Таблиця термінів", callback_data="emex_terms"))
    with open('emex/attachments/emex_option.jpg', 'rb') as photo:
        await message.answer_photo(photo, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "⚙️AUTONOVA")
async def show_autonova_options(message: types.Message):
    keyboard = InlineKeyboardMarkup()
    keyboard.add(InlineKeyboardButton("Завантажити прайс", callback_data="autonova_load_prices"))
    keyboard.add(InlineKeyboardButton("Завантаження за розкладом", callback_data="autonova_schedule"))
    with open('autonova/attachments/autonova_option.jpg', 'rb') as photo:
        await message.answer_photo(photo, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "📖Документація ABS-bot")
async def show_autonova_options(message: types.Message):
    with open('attachments/documentation.docx', 'rb') as doc:
        await message.answer_document(doc)


@dp.callback_query_handler(lambda callback_query: callback_query.data == "emex_load_prices")
async def action1(callback_query: types.CallbackQuery):
    await callback_query.answer("Завантаження...")
    loading_jpg_path = "attachments/progress-loading-bar.jpg"
    with open(loading_jpg_path, 'rb') as jpg_file:
        loading_message = await bot.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=jpg_file,
            caption="⏳ LOADING...Please wait"
        )
    result = EmexMain().main()
    await loading_message.delete()
    await callback_query.message.answer(result, parse_mode='HTML')


@dp.callback_query_handler(lambda callback_query: callback_query.data == "emex_schedule")
async def action2(callback_query: types.CallbackQuery):
    await toggle_schedule(callback_query, 'emex')


@dp.callback_query_handler(lambda callback_query: callback_query.data == "emex_terms")
async def action_get_data(callback_query: types.CallbackQuery):
    await callback_query.message.answer_photo(InputFile('emex/attachments/terms.jpg'), parse_mode='HTML')


@dp.callback_query_handler(lambda callback_query: callback_query.data == "autonova_load_prices")
async def action3(callback_query: types.CallbackQuery):
    await callback_query.answer("Завантаження...")
    loading_jpg_path = "attachments/progress-loading-bar.jpg"
    with open(loading_jpg_path, 'rb') as jpg_file:
        loading_message = await bot.send_photo(
            chat_id=callback_query.message.chat.id,
            photo=jpg_file,
            caption="⏳ LOADING...Please wait"
        )
    result = AutonovaMain().main()
    await loading_message.delete()
    await callback_query.message.answer(result, parse_mode='HTML')


@dp.callback_query_handler(lambda callback_query: callback_query.data == "autonova_schedule")
async def action4(callback_query: types.CallbackQuery):
    await toggle_schedule(callback_query, 'autonova')


@dp.message_handler(lambda message: message.text == "Special Option")
async def go_special(message: types.Message):
    await message.answer("Special Option Done")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
