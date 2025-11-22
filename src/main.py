import asyncio
import config
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from handlers.message_handlers import router

bot = Bot(config.BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())