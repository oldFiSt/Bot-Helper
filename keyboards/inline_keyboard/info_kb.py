from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .actions_cb import random_num_cb_update

random_site_cb_data = "random_site_cb_data"
random_num_cb = "random_num_cb"
random_new_num_cb = "random_new_num_cb"


def create_info_kb() -> InlineKeyboardMarkup:
    tg_channel_btn = InlineKeyboardButton(text="👀Разработчик 1️⃣", url="https://t.me/oldFiSt")
    tg_channel_btn_second = InlineKeyboardButton(text="👀Разработчик 2️⃣", url="https://t.me/Sergeik22")
    btn_third = InlineKeyboardButton(text="random num update", callback_data=random_num_cb_update)
    btn_fourd = InlineKeyboardButton(text="Random num", callback_data=random_num_cb)
    btn_five = InlineKeyboardButton(text="Random new number", callback_data=random_new_num_cb)
    row_first = [tg_channel_btn]
    row_second = [tg_channel_btn_second]
    row_third = [btn_third]
    row_btn_fourd = [btn_fourd]
    row_btn_five = [btn_five]
    rows = [row_first, row_second, row_third, row_btn_fourd, row_btn_five]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup
