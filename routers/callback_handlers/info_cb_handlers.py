
from aiogram import Router, F
from aiogram.types import CallbackQuery
from random import randint

from keyboards.inline_keyboard.info_kb import random_site_cb_data, random_num_cb, random_new_num_cb


router = Router(name=__name__)

@router.callback_query(F.data == random_site_cb_data)
async def handle_random_site(callback_query: CallbackQuery):
    bot_me = await callback_query.bot.me()
    await callback_query.answer(
        url=f"t.me/{bot_me.username}?start={randint(1, 100)}"
    )



@router.callback_query(F.data == random_new_num_cb)
async def handle_random_new_num(callback_query: CallbackQuery):
    await callback_query.answer(text=f" random: {randint(1, 23)}", show_alert=True)