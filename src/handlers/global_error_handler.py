from src.main import dp
import logging

@dp.errors_handler()
async def global_error_handler(update, exception):
    logging.exception(f"Ошибка при обработке апдейта {update}: {exception}")
    return True