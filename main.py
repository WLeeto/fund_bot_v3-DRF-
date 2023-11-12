from create_bot import bot
from create_logger import logger

from misc.utils import set_default_commands
from create_bot import dp
import asyncio


async def start():
    """
    Запуск бота
    """
    await set_default_commands()
    logger.info('Бот запущен')


async def shutdown():
    """
    Завершение работы
    """
    logger.warning('Бот отключен')


from handlers import client, admin, other

admin.register_handlers_admin(dp)
client.register_handlers_client(dp)
other.register_handlers_other(dp)


async def main():
    await start()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
