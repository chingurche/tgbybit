from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from states import Form
from states import PersonalDataForm
from user_data import UserData
from exceptions import UserIsNotFound
from personal_data import PersonalData
import keyboard

router = Router()

# Главное меню

@router.message(F.text == "/start")
@router.message(F.text == keyboard.BUTTONS_TEXT["back"])
async def display_main_page_msg(msg: Message, state: FSMContext):
    await state.set_state(Form.main_page)
    
    try:
        user = UserData(msg.from_user.id) # здесь UserIsNotFound

        await msg.answer(
            f"Твой профиль: \n\n" \
            f"{user.personal_data.name}, из группы {user.personal_data.student_group} - @{msg.from_user.username}\n" \
            f"{user.get_string_tags()}",
            reply_markup=keyboard.main_keyboard
        )
    except UserIsNotFound:
        await msg.answer("Привет, давай зарегистрируемся")
        await collect_personal_data(msg, state)

@router.callback_query(lambda c: c.data == "goto_main_page")
async def display_main_page_cb(query: CallbackQuery, state: FSMContext):
    await display_main_page_msg(query.message)

# Поиск 

@router.message(Form.main_page, F.text == keyboard.BUTTONS_TEXT["search_by_merge_tags"])
async def display_random_person(msg: Message, state: FSMContext):
    await state.set_state(Form.search_by_merge_page)
    
    user = UserData.get_random(msg.from_user.id)
    await msg.answer(
            f"{user.personal_data.name}, из группы {user.personal_data.student_group}\n" \
            f"{user.get_string_tags()}",
        reply_markup=keyboard.swiping_keyboard
    )

# Персональные данные

@router.message(Form.main_page, F.text == keyboard.BUTTONS_TEXT["edit"])
async def collect_personal_data(msg: Message, state: FSMContext):
    await msg.answer(
        "Введи новый никнейм",
        reply_markup = ReplyKeyboardRemove()
    )
    await state.set_state(PersonalDataForm.set_name)

@router.message(PersonalDataForm.set_name)
async def set_name(msg: Message, state: FSMContext):
    await state.update_data(name = msg.text)
    
    await msg.answer("Из какой ты группы?")
    await state.set_state(PersonalDataForm.set_student_group)

@router.message(PersonalDataForm.set_student_group)
async def set_student_group(msg: Message, state: FSMContext):
    await state.update_data(student_group = msg.text)
    
    data = await state.get_data()
    personal_data = PersonalData(data["name"], data["student_group"])
    UserData.update_personal_data(msg.from_user.id, personal_data)

    await msg.answer("Персональные данные были обновлены")
    
    await display_main_page_msg(msg, state)