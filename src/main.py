import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.message_handlers import router

TOKEN = "8272034294:AAFJhoN2RmPP5QEThj9g1yTZ3gmrqtb-UkI"

bot = Bot(TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())