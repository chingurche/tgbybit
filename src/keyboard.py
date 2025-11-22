
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

BUTTONS_TEXT = {
    #"search_by_merge_tags": "Поиск по общим тегам",
    "search_by_merge_tags": "Найти рандомного пользователя (test)",
    "next_user": "Дальше",
    "search_by_tag": "Поиск по исполнителю",
    "edit_tags": "Изменить исполнителей",
    "add_tag": "Добавить исполнителя",
    "remove_tag": "Удалить исполнителя",
    "edit_data": "Изменить данные",
    "top_tags": "Топ исполнителей",
    "help": "Помощь",
    "back": "Вернуться"
}

main = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = BUTTONS_TEXT["search_by_merge_tags"])],
        [KeyboardButton(text = BUTTONS_TEXT["search_by_tag"])],
        [KeyboardButton(text = BUTTONS_TEXT["edit_data"]), KeyboardButton(text = BUTTONS_TEXT["edit_tags"])],
        [KeyboardButton(text = BUTTONS_TEXT["help"]), KeyboardButton(text = BUTTONS_TEXT["top_tags"])],
    ],
    resize_keyboard=True
)

swiping = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = BUTTONS_TEXT["next_user"])],
        [KeyboardButton(text = BUTTONS_TEXT["back"])]
    ],
    resize_keyboard=True
)

tags = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text = BUTTONS_TEXT["add_tag"])],
        [KeyboardButton(text = BUTTONS_TEXT["remove_tag"])],
        [KeyboardButton(text = BUTTONS_TEXT["back"])]
    ],
    resize_keyboard=True
)