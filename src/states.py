from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    main_page = State()
    search_by_merge_page = State()
    change_personal_data = State()


class PersonalDataForm(StatesGroup):
    set_name = State()
    set_student_group = State()