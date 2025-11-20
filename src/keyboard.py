
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BUTTONS_TEXT = {
    #"search_by_merge_tags": "Поиск по общим тегам",
    "search_by_merge_tags": "Найти рандомного пользователя (test)",
    "edit": "Изменить персональные данные",
    "back": "Вернуться"
}

main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = BUTTONS_TEXT["search_by_merge_tags"])],
        [KeyboardButton(text = "Поиск по тегу")],
        [KeyboardButton(text = "Изменить свои теги")],
        [KeyboardButton(text = BUTTONS_TEXT["edit"])]
    ]
)

swiping_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = "Отправить реквест"), KeyboardButton(text = "Дальше")],
        [KeyboardButton(text = BUTTONS_TEXT["back"])]
    ]
)