from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


DOWN = "Down"

class ButtonText:
    TRAINING = "Составить тренировку 💪"
    EAT = "Составить питание 👨🏻‍🍳 "
    KBY = "Рассчитать КБЖУ 🧮"
    LOSS = "Похудение"
    UP = "Набор массы"
    CURRENT = "Поддержание массы"


def get_on_start_kb():
    button_first = KeyboardButton(text=ButtonText.KBY)
    button_second = KeyboardButton(text=ButtonText.EAT)
    buttons_first_row = [button_first]
    buttons_second_row = [button_second]
    markup = ReplyKeyboardMarkup(keyboard=[buttons_first_row], resize_keyboard=True)
    return markup


def get_on_kby_kb():
    button_first = KeyboardButton(text=ButtonText.LOSS)
    button_second = KeyboardButton(text=ButtonText.UP)
    button_thrird = KeyboardButton(text=ButtonText.CURRENT)
    buttons_first_row = [button_first]
    buttons_second_row = [button_second]
    buttons_thrird_row = [button_thrird]
    markup = ReplyKeyboardMarkup(keyboard=[buttons_first_row,buttons_second_row, buttons_thrird_row], resize_keyboard=True,
                                 one_time_keyboard=True )# чтобы клавиатура удалилась после нажатия
    return markup

