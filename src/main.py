import asyncio
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.message_handlers import router, bot

dp = Dispatcher(storage=MemoryStorage())

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())