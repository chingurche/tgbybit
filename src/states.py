from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    main_page = State()
    search_by_merge_page = State()
    change_personal_data_page = State()
    change_tags_page = State()

class SearchingForm(StatesGroup):
    ask_tag = State()
    next_found_user = State()

class ConnectsForm(StatesGroup):
    next_connect = State()

class ClearConnectsForm(StatesGroup):
    confirmation = State()

class PersonalDataForm(StatesGroup):
    set_name = State()
    set_student_group = State()

class TagsForm(StatesGroup):
    add_tag = State()
    remove_tag = State()