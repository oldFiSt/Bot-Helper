from aiogram import Router, Dispatcher, types, F
from aiogram.enums import ParseMode, ChatAction
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from func_kbjy import calculate_kbju

from keyboards.common_keyboard import ButtonText, get_on_start_kb, get_on_kby_kb
from keyboards.inline_keyboard.info_kb import create_info_kb
from keyboards.common_keyboard import DOWN
from aiogram.types import CallbackQuery

from keyboards.inline_keyboard.actions_cb import create_action_kb
from keyboards.common_keyboard import ButtonText
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup

from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

from Data_Base.connect import db



dp = Dispatcher()#ловит сообщения
router = Router()


class UserStates(StatesGroup):
    waiting_height = State()
    waiting_weight = State()
    waiting_age = State()
    waiting_gender = State()


@router.message(CommandStart())
async def handle_start(message: types.Message):
    user_data = db.get_user(message.from_user.id)

    if user_data:
        # Если пользователь уже есть в базе
        welcome_text = markdown.text(
            markdown.text(markdown.bold((message.from_user.full_name)), f"\\,с возвращением😃\\!"),
            f"Рады видеть вас снова\\!",
            f"Ваши последние сохраненные данные\\:",
            markdown.text(f"• Рост\\: {user_data['height']} см"),
            markdown.text(f"• Вес\\: {user_data['weight']} кг"),
            markdown.text(f"• Возраст\\: {user_data['age']} лет"),
            markdown.text(f"• Пол\\: {user_data['gender']}"),
            f"Для новых расчетов нажмите на кнопку КБЖУ ниже⬇️",
            sep="\n"
        )
    else:
        # Новый пользователь
        welcome_text = markdown.text(
            markdown.text(markdown.bold((message.from_user.full_name)), f"\\,привет😃\\!"),
            f"Добро пожаловать в наш бот",
            f"Я помогу тебе составить тренировки и питание\\.\\.\\.",
            f"Для начала давай рассичтаем необходимое КБЖУ",
            f"для твоих данных\\.",
            f"Для этого нажми на соответсвующую кнопку ниже⬇️",
            sep="\n"
        )


    markup = get_on_start_kb()
    text = welcome_text
    await message.answer(text = text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=markup,)


@router.message(F.text == ButtonText.KBY)
async def handle_kby(message: types.Message):
    markup = get_on_kby_kb()
    text = markdown.text(
        "Давай рассчитаем твоё КБЖУ ",

        "Для этого выбери нужную цель\\:",
        markdown.text(
            markdown.bold("Похудение")
        ),
        markdown.text(
            markdown.bold("Набор массы")
        ),
        markdown.text(
            markdown.bold("Поддержание веса")
        ),
        sep="\n"
    )
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=markup)

#на случай, если нужно удалить клавиатуру
# @router.message(F.text == ButtonText.CLOZE)
# async def handle_close(message: types.Message):
#     await message.answer(
#         text= "Вы закрыли окно. Если хотите ввести данные заново напишите /start",
#         reply_markup=ReplyKeyboardRemove(),
#     )


@router.message(F.text == ButtonText.LOSS)
async def handle_loss(callback_query: CallbackQuery, state: FSMContext):
    await callback_query.answer(text="Введите ваш рост (в см)")
    await state.set_state(UserStates.waiting_height)

@router.message(F.text == ButtonText.UP)
async def handle_gain(message: types.Message, state: FSMContext):
    await state.update_data(goal='gain')
    await message.answer("Введите ваш рост (в см):")
    await state.set_state(UserStates.waiting_height)

@router.message(F.text == ButtonText.CURRENT)
async def handle_maintain(message: types.Message, state: FSMContext):
    await state.update_data(goal='maintain')
    await message.answer("Введите ваш рост (в см):")
    await state.set_state(UserStates.waiting_height)



@router.message(UserStates.waiting_height)
async def process_height(message: types.Message, state: FSMContext):
    try:
        height = int(message.text)
        if height < 50 or height > 250:
            await message.answer("Пожалуйста, введите корректный рост (50-250 см):")
            return

        await state.update_data(height=height)
        await message.answer("Теперь введите ваш вес (в кг):")
        await state.set_state(UserStates.waiting_weight)

    except ValueError:
        await message.answer("Пожалуйста, введите число для роста:")


@router.message(UserStates.waiting_weight)
async def process_weight(message: types.Message, state: FSMContext):
    try:
        weight = float(message.text)
        if weight < 20 or weight > 300:
            await message.answer("Пожалуйста, введите корректный вес (20-300 кг):")
            return

        await state.update_data(weight=weight)
        await message.answer("Теперь введите ваш возраст:")
        await state.set_state(UserStates.waiting_age)

    except ValueError:
        await message.answer("Пожалуйста, введите число для веса:")


@router.message(UserStates.waiting_age)
async def process_age(message: types.Message, state: FSMContext):
    try:
        age = int(message.text)
        if age < 1 or age > 120:
            await message.answer("Пожалуйста, введите корректный возраст (1-120 лет):")
            return

        await state.update_data(age=age)

        # Создаем клавиатуру для выбора пола
        gender_markup = ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="Мужской"), KeyboardButton(text="Женский")]
            ],
            resize_keyboard=True,
            one_time_keyboard=True
        )

        await message.answer("Выберите ваш пол:", reply_markup=gender_markup)
        await state.set_state(UserStates.waiting_gender)

    except ValueError:
        await message.answer("Пожалуйста, введите число для возраста:")


@router.message(UserStates.waiting_gender)
async def process_gender(message: types.Message, state: FSMContext):
    gender = message.text.lower()

    if gender not in ['мужской', 'женский', 'male', 'female']:
        await message.answer("Пожалуйста, выберите пол из предложенных вариантов: мужской или женский")
        return

    # Получаем данные из состояния
    user_data = await state.get_data()
    height = user_data.get('height')
    weight = user_data.get('weight')
    age = user_data.get('age')
    goal = user_data.get('goal', 'maintain')

    db.add_user(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        height=height,
        weight=weight,
        age=age,
        gender=gender,
        goal=goal
    )

    # Рассчитываем КБЖУ
    kbju_data = calculate_kbju(
        height=height,
        weight=weight,
        age=age,
        gender='male' if gender == 'мужской' else 'female',
        goal=goal
    )

    goal_texts = {
        'loss': 'похудения',
        'gain': 'набора массы',
        'maintain': 'поддержания веса'
    }

    response = (
        f"🏆 Ваша суточная норма КБЖУ для {goal_texts.get(goal, 'поддержания веса')}:\n\n"
        f"🔥 Калории: {kbju_data['calories']} ккал\n"
        f"🥩 Белки: {kbju_data['protein']} г\n"
        f"🥑 Жиры: {kbju_data['fat']} г\n"
        f"🍚 Углеводы: {kbju_data['carbs']} г\n\n"
        f"📊 Дополнительная информация:\n"
        f"• Базовый метаболизм: {kbju_data['bmr']} ккал\n"
        f"• Общий расход: {kbju_data['tdee']} ккал\n\n"
        f"💡 Советы:\n"
        f"• Пейте достаточно воды\n"
        f"• Распределите приемы пищи равномерно\n"
        f"• Учитывайте свою активность\n\n"
        f"✅ Ваши данные сохранены! Используйте /start для быстрого доступа."
    )

    await message.answer(response, reply_markup=ReplyKeyboardRemove())
    await state.clear()


@router.message(Command("mydata"))
async def handle_mydata(message: types.Message):
    user_data = db.get_user(message.from_user.id)

    if not user_data:
        await message.answer("У вас нет сохраненных данных. Используйте /start для начала работы.")
        return

    response = (
        f"📋 Ваши сохраненные данные:\n\n"
        f"📏 Рост: {user_data['height']} см\n"
        f"⚖️ Вес: {user_data['weight']} кг\n"
        f"🎂 Возраст: {user_data['age']} лет\n"
        f"🚻 Пол: {user_data['gender']}\n"
        f"🎯 Цель: {user_data['goal']}\n\n"
        f"Для новых расчетов используйте кнопку КБЖУ"
    )

    await message.answer(response)


@router.callback_query(F.data == DOWN)
async def handle_down(callback_query: CallbackQuery):
    await callback_query.answer(text="ХУДЕЙ")



@router.message(Command("action", prefix="/!"))
async def handle_actions(message: types.Message):
    markup = create_action_kb()
    await message.answer(
        text= "Разработчики: ",
        reply_markup=markup,
    )


@router.message(Command("help"))
async def handle_help(message: types.Message):
    text = markdown.text(
        "🤖Fitnes\\-Bot твой персональный фитнес\\-трекер\\!",
        "Рассчитаю калории и БЖУ\\, составлю план тренировок и питания под твою цель\\:",
        markdown.text(
            markdown.bold("✅Похудение")
        ),
        markdown.text(
            markdown.bold("✅Набор массы")
        ),
        markdown.text(
            markdown.bold("✅Поддержание веса")
        ),
        "Всё просто\\, эффективно и персонализировано\\. Начни трансформацию прямо сейчас\\!💪",
        sep="\n"
    )
    await message.bot.send_chat_action(
        chat_id=message.chat.id,
        action= ChatAction.TYPING,
    ) # уведомление сверху для ожидания
    await message.answer(text=text, parse_mode=ParseMode.MARKDOWN_V2)
