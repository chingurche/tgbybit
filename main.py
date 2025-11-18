from aiogram import Bot, Dispatcher, Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from testbase import UserRepository

bot = Bot("8427610229:AAE9mUs_RYLF2Cbng1H-0TGeRirYLrK4A4k")
dp = Dispatcher(storage=MemoryStorage())
router = Router()
dp.include_router(router)

repository = UserRepository("users.db")

class Form(StatesGroup):
    main_page = State()
    change_personal_data = State()


class PersonalDataForm(StatesGroup):
    set_name = State()
    set_student_group = State()

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

edit_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Поиск по общим тегам", callback_data="goto_random_person")],
        [InlineKeyboardButton(text="Поиск по тегу", callback_data="goto_personal_data")],
        [InlineKeyboardButton(text="Изменить свои теги", callback_data="goto_personal_data")],
        [InlineKeyboardButton(text="Изменить персональные данные", callback_data="goto_personal_data")]
    ]
)

swiping_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Запросить юз", callback_data="goto_main_page")],
        [InlineKeyboardButton(text="Следующий", callback_data="goto_main_page")],
        [InlineKeyboardButton(text="Вернуться", callback_data="goto_main_page")]
    ]
)

@router.callback_query(lambda c: c.data == "goto_random_person")
async def display_random_person(query: CallbackQuery, state: FSMContext):
    msg = query.message
    user = repository.get_random_user()
    _, username, student_group = user
    await msg.edit_text(f"{username} : {student_group}", reply_markup=swiping_keyboard)

@router.message(Command("start"))
async def display_main_page_msg(msg: Message):
    user = repository.get_user(msg.from_user.id)
    if user is None:
        await msg.answer("Профиль не создан. Для того чтобы отправлять запросы другим пользователям" \
        " заполните персональные данные и теги", reply_markup=edit_keyboard)
    else:
        _, username, student_group = user
        await msg.answer(f"{username} : {student_group}", reply_markup=edit_keyboard)

@router.callback_query(lambda c: c.data == "goto_main_page")
async def display_main_page_cb(query: CallbackQuery, state: FSMContext):
    await display_main_page_msg(query.message)

# Персональные данные

@router.callback_query(lambda c: c.data == "goto_personal_data")
async def collect_personal_data(query: CallbackQuery, state: FSMContext):
    await state.set_state(PersonalDataForm.set_name)
    await query.message.edit_text("Введи никнейм")
    await query.answer()

@router.message(PersonalDataForm.set_name)
async def set_name(msg: Message, state: FSMContext):
    await state.update_data(name = msg.text)
    
    await msg.answer("Из какой ты группы?")
    await state.set_state(PersonalDataForm.set_student_group)

@router.message(PersonalDataForm.set_student_group)
async def set_student_group(msg: Message, state: FSMContext):
    await state.update_data(student_group = msg.text)
    
    data = await state.get_data()
    await state.set_state(Form.main_page)
    repository.add_or_update_user(msg.from_user.id, data['name'], data['student_group'])

    await msg.answer("Персональные данные были обновлены")
    
    await display_main_page_msg(msg)

async def main():
    await dp.start_polling(bot)

asyncio.run(main())
