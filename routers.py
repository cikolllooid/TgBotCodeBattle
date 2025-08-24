from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from keyboards import main_but
from datetime import datetime
from db import get_connection

connection = get_connection()

router = Router()

class Reg(StatesGroup):
    avatar = State()
    name = State()
    bio = State()

@router.message(CommandStart())
async def start_cmd(message: Message):
    text = (
        f"🔥 Привет, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в *CodeBattle* — арену, где код решает всё.\n\n"
        "💻 Здесь ты сможешь:\n"
        "• Сражаться с другими программистами в кодовых дуэлях\n"
        "• Писать проекты и получать оценки\n"
        "• Прокачивать рейтинг и зарабатывать уважение комьюнити\n\n"
        "⚡ Напиши /help, чтобы узнать правила и начать битву!"
    )
    await message.answer(text, parse_mode="Markdown")

@router.message(Command("reg"))
async def reg(message: Message, state: FSMContext):
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """SELECT tg_id FROM public.users WHERE tg_id = %s""",
                (message.from_user.id,)
            )
            telegram_id = cursor.fetchone()[0]

        if telegram_id:
            await message.answer("Вы уже зарегестрированы", reply_markup=main_but)
            return
    except Exception as e:
        print(e)
    await state.set_state(Reg.avatar)
    await message.answer("Отправьте вашу аватарку")

@router.message(Reg.avatar, F.photo)
async def reg_name(message: Message, state: FSMContext):
    path = rf"C:\Users\Eugen\PycharmProjects\tgAPP\backend\static\imgs_avatars\{message.from_user.id}.jpg"
    photo = message.photo[-1].file_id

    await message.bot.download(file=photo, destination=path)
    await state.update_data(avatar=path)
    await state.set_state(Reg.name)
    await message.answer("Введите название профиля")

@router.message(Reg.name)
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Reg.bio)
    await message.answer("Введите описание профиля")

@router.message(Reg.bio)
async def reg_bio(message: Message, state: FSMContext):
    await state.update_data(bio=message.text)
    user_id = message.from_user.id
    data = await state.get_data()
    try:
        if message.from_user.id == 1251098499:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO users (tg_id, avatar_path, name, bio, elo, is_admin, solved, join_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (user_id, data['avatar'], data['name'], data['bio'], 200, True, 0, datetime.now().date())
                )
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO users (tg_id, avatar_path, name, bio, elo, is_admin, solved, join_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
                    (user_id, data['avatar'], data['name'], data['bio'], 200, False, 0, datetime.now().date())
                )

    except Exception as e:
        print(e)

    await message.answer("Регистрация завершена", reply_markup=main_but)
    await state.clear()
