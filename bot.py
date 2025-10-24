import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown  #для работы с разметкой(видео 2)
from aiogram.enums import ParseMode #для работы с разметкой(видео 2)
import config


#СООБЩЕНИЯ ОБРАБАТЫВАЮТСЯ СВЕРХУ ВНИЗ
dp = Dispatcher()#ловит сообщения


@dp.message(CommandStart())
async def handle_start(message: types.Message):
    text = markdown.text(

        markdown.text(markdown.bold((message.from_user.full_name)), f"привет😃\\!"),
        f"Добро пожаловать в наш бот",
        f"Выбери что ты хочешь сделать\\.\\.\\.\n ",
        sep="\n"
    )
    # fullname = message.from_user.full_name
    # lenght_name = len(fullname)
    # text = (f"{message.from_user.full_name}, привет😃! \n"
    #                           f"Добро пожаловать в наш бот\n"
    #                           f"Выбери что ты хочешь сделать...\n ")
    # entity_bold = types.MessageEntity(type= "bold", offset=0, length=lenght_name)
    # entities = [entity_bold]
    await message.answer(text = text, parse_mode=ParseMode.MARKDOWN_V2)



@dp.message(Command("help"))
async def handle_help(message: types.Message):
    text = markdown.text(
        "🤖Я бот помощник в составлении тренировок и питания",
        "Выбери нужную цель\\:",
        markdown.text(
            markdown.bold("Похудение")
        ),
        markdown.text(
            markdown.bold("Набор массы")
        ),
        markdown.text(
            markdown.bold("Поддержание веса")
        ),
        "Введи необходимые данные и получи тренировку\\.",
        sep="\n"
    )
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


@dp.message()
async def echo_message(message: types.Message):
    # await bot.send_message(
    #     chat_id=message.chat.id,
    #     text= "Wait a second... ",
    # )
    # await message.reply(text=message.text) #отвечает на сообщение
    # await message.answer(text= message.text) #без ответа на сообщение
    if message.text:
        await message.answer(
            text=message.text,
            entities=message.entities,
        )
    elif message.sticker:
        await message.reply_sticker(sticker=message.sticker.file_id)
    else:
        await message.reply(text="This is wrong data")



async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
