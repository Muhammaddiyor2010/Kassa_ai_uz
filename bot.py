import asyncio
import logging

from aiogram import  Dispatcher

from handlers.echo import router
from handlers.start import start_router
from handlers.chiqim import chiqim_router
from handlers.kirim import kirim_router
from handlers.report import report_router
from loader import bot,  db

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.INFO,
       
    )
    # db.create_table_users()
    # db.create_table_chiqim()
    # db.create_table_kirim()
    
    logger.info("Starting bot")


    dp: Dispatcher = Dispatcher()

    dp.include_routers( 
        chiqim_router,
        kirim_router,
        report_router,
        start_router,
        # router
    )



        
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
