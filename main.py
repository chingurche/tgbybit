import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import router
from onboarding_handler import onboarding_router

async def main():
    bot = Bot("8427610229:AAE9mUs_RYLF2Cbng1H-0TGeRirYLrK4A4k")
    dp = Dispatcher(storage=MemoryStorage())

    #dp.include_router(onboarding_router)
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
