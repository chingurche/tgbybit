from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from handlers import PersonalDataForm
from handlers import repository

onboarding_router = Router()

@onboarding_router.message(F.text)
async def onboarding_handler(msg: Message, state: FSMContext):
    current_state = await state.get_state()
    user = repository.get_user(msg.from_user.id)

    if user is not None or current_state is not None:
        return 
    
    await msg.answer("Привет, давай зарегистрируемся. Введи свой никнейм")
    await state.set_state(PersonalDataForm.set_name)