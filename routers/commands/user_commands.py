from aiogram import Router, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils import markdown
from aiogram.utils import markdown  #для работы с разметкой(видео 2)
from aiogram.enums import ParseMode, ChatAction #для работы с разметкой(видео 2)
from aiogram.utils.chat_action import ChatActionSender

from config import ADMIN_TOKEN

router = Router()
dp = Dispatcher()

@router.message(Command("code", prefix="/!"))
async def handle_command_code(message: types.Message):
    text = markdown.text(
        "Here's Python code:",
        markdown.markdown_decoration.pre_language(
                "print('Hello world')",
             language="python"
        ),
        sep="\n"
    )
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)


@router.message(F.photo)
async def handle_photo(message: types.Message):
    await message.reply(text="Не понимаю фото. Отправь текст😡😡😡")


@router.message(F.text == "!admin" * F.from_user.id.in_({42, 1000, 718161465}))
async def admin_func(message: types.Message):
    await message.reply(text="Привет, админ 👑")

@router.message(F.text == "!gym")
async def admin_func(message: types.Message):
    await message.bot.send_video(
        chat_id=message.chat.id,
        video=types.FSInputFile('video/supino.mp4'),
        caption="Держи технику для жима лёжа",
    )


async def send_bid_data(message: types.Message):
    name = take_name(2, result)
    await message.answer(text= name)



@router.message(F.text == "/big")
async def big_file(message: types.Message):
    await message.answer(text= "Опрашиваю Базу данных")
    await message.bot.send_chat_action(
        chat_id= message.chat.id,
        action= ChatAction.TYPING,
    )
    action_sender = ChatActionSender(
         bot = message.bot,
         chat_id=message.chat.id,
         action=ChatAction.TYPING,
    )
    async with action_sender:
        await send_bid_data(message)



