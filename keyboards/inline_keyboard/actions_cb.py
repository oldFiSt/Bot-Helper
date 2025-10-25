from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
random_num_cb_update = "random_num_cb_update"


def create_action_kb(random_number_text="👀Random number 1️⃣") -> InlineKeyboardMarkup:
    btn_rnd = InlineKeyboardButton(text=random_number_text, callback_data=random_num_cb_update)
    row_first = [btn_rnd]
    rows = [row_first]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup
