import asyncio
import logging

from aiogram import Bot, F, Dispatcher, Router
from aiogram import types
from aiogram.filters import Command
from aiogram.utils import markdown  #для работы с разметкой(видео 2)
from aiogram.enums import ParseMode, ChatAction #для работы с разметкой(видео 2)
from aiogram.utils.chat_action import ChatActionSender

import config

from routers import router as main_router
from routers.commands.user_commands import dp

dp.include_router(main_router)
# message.from_user.id узнать id пользователя
#СООБЩЕНИЯ ОБРАБАТЫВАЮТСЯ СВЕРХУ ВНИЗ

async def main():
    logging.basicConfig(level=logging.INFO)
    bot = Bot(token=config.BOT_TOKEN)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
