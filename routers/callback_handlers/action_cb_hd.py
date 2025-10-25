from aiogram import Router, F
from random import randint
from keyboards.inline_keyboard.actions_cb import create_action_kb
from aiogram.types import CallbackQuery
random_num_cb = "random_num_cb"

router = Router(name=__name__)

@router.callback_query(F.data == random_num_cb)
async def handle_random_number_edit(callback_query: CallbackQuery):
    await callback_query.answer()
    callback_query.message.edit_text( text=f"Random number: {randint(1, 100)}", reply_markup= create_action_kb("Generate "))
