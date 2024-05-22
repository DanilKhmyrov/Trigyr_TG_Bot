import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher


from app.handlers import router

from config import config


async def main():
    bot = Bot(token=config.bot_token.get_secret_value())
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, stream=sys.stdout)
    logging.debug('Запускаю бота...')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен')
