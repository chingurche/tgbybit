from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from aiogram.types import CallbackQuery

from states import Form, PersonalDataForm, TagsForm, SearchingForm
from user_data import UserData, PersonalData, TagList
from exceptions import UserIsNotFound, NoUsersWithTagError
import keyboard

router = Router()

# Поиск рандомного

@router.message(Form.main_page, F.text == keyboard.BUTTONS_TEXT["search_by_merge_tags"])
async def display_random_person(msg: Message, state: FSMContext):
    await state.set_state(Form.search_by_merge_page)
    
    other_user = UserData.get_random(msg.from_user.id)
    my_user = UserData(msg.from_user.id)
    await msg.answer(
        other_user.display_compared_with(my_user, anonymous=True),
        parse_mode="MarkdownV2",
        reply_markup=keyboard.swiping
    )

# Поиск по одному тегу

@router.message(Form.main_page, F.text == keyboard.BUTTONS_TEXT["search_by_tag"])
async def ask_tag(msg: Message, state: FSMContext):
    await state.set_state(SearchingForm.ask_tag)

    await msg.answer(
        "По какому исполнителю будем искать?",
        reply_markup = ReplyKeyboardRemove()
    )
    
@router.message(SearchingForm.ask_tag)
async def ask_tag(msg: Message, state: FSMContext):
    try:
        users = UserData(msg.from_user.id).get_list_of_users_by_tag(msg.text)
        await state.update_data(founded_users = users)
        await msg.answer(
            f"Слушателей исполнителя _{msg.text}_ найдено: {len(users)}",
            parse_mode="MarkdownV2"
        )
        await next_user(msg, state)
    except NoUsersWithTagError:
        await msg.answer("Не найдено слушателей кроме тебя")
        await display_main_page_msg(msg, state)
    except TypeError:
        await msg.answer("Не найдено слушателей")
        await display_main_page_msg(msg, state)

@router.message(SearchingForm.next_found_user, F.text == keyboard.BUTTONS_TEXT["next_user"])
async def next_user(msg: Message, state: FSMContext):
    await state.set_state(SearchingForm.next_found_user)

    data = await state.get_data()
    users = data["founded_users"]
    if len(users) == 0:
        await msg.answer("Слушатели закончились")
        await display_main_page_msg(msg, state)
        return
    found_user_id = users.pop(0)
    found_user = UserData(found_user_id)
    await state.update_data(founded_users = users)
    await state.update_data(found_user_id = found_user_id)

    my_user = UserData(msg.from_user.id)
    await msg.answer(
        found_user.display_compared_with(my_user, anonymous=True),
        parse_mode="MarkdownV2",
        reply_markup=keyboard.swiping 
    )


@router.message(SearchingForm.next_found_user, F.text == keyboard.BUTTONS_TEXT["send_request"])
async def send_request(msg: Message, state: FSMContext):
    found_user_id = await state.get_data()["found_user_id"]
    found_user = UserData(found_user_id)
    found_user.send_request_from(msg.from_user.id)
    await msg.answer("✅ Запрос отправлен, ждем ответа...")

    await next_user(msg, state)

# Посмотреть запросы


# Теги

@router.message(Form.main_page, F.text == keyboard.BUTTONS_TEXT["edit_tags"])
async def change_tags(msg: Message, state: FSMContext):
    await state.set_state(Form.change_tags_page)

    user = UserData(msg.from_user.id)
    await msg.answer(
        f"{user.tag_list.get_as_mine()}",
        parse_mode="MarkdownV2",
        reply_markup = keyboard.tags
    )

@router.message(Form.change_tags_page, F.text == keyboard.BUTTONS_TEXT["add_tag"])
async def ask_new_tag(msg: Message, state: FSMContext):
    await state.set_state(TagsForm.add_tag)

    await msg.answer(
        "Введи нового исполнителя",
        reply_markup = ReplyKeyboardRemove()
    )

@router.message(TagsForm.add_tag)
async def add_new_tag(msg: Message, state: FSMContext):
    UserData(msg.from_user.id).add_new_tag(msg.text)

    await change_tags(msg, state)


@router.message(Form.change_tags_page, F.text == keyboard.BUTTONS_TEXT["remove_tag"])
async def ask_tag(msg: Message, state: FSMContext):
    await state.set_state(TagsForm.remove_tag)

    await msg.answer(
        "Какого исполнителя хочешь удалить из профиля?",
        reply_markup = ReplyKeyboardRemove()
    )

@router.message(TagsForm.remove_tag)
async def add_tag(msg: Message, state: FSMContext):
    try:
        UserData(msg.from_user.id).remove_tag(msg.text)
    except:
        await msg.answer("У тебя нет такого исполнителя")
    
    await change_tags(msg, state)

# Персональные данные

@router.message(Form.main_page, F.text == keyboard.BUTTONS_TEXT["edit_data"])
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

# Топ тегов

@router.message(Form.main_page, F.text == keyboard.BUTTONS_TEXT["top_tags"])
async def ask_tag(msg: Message, state: FSMContext):
    await msg.answer(
        TagList.get_popular(),
        parse_mode="MarkdownV2"
    )

# Главное меню

@router.message()
@router.message(F.text == keyboard.BUTTONS_TEXT["back"])
async def display_main_page_msg(msg: Message, state: FSMContext):
    await state.set_state(Form.main_page)
    
    try:
        user = UserData(msg.from_user.id) # здесь UserIsNotFound

        await msg.answer(
            user.display_as_me(),
            parse_mode="MarkdownV2",
            reply_markup=keyboard.main
        )
    except UserIsNotFound:
        await msg.answer("Привет, давай зарегистрируемся")
        await collect_personal_data(msg, state)

@router.callback_query(lambda c: c.data == "goto_main_page")
async def display_main_page_cb(query: CallbackQuery, state: FSMContext):
    await display_main_page_msg(query.message)