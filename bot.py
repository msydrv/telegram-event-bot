import asyncio
import logging
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers.common import router
from handlers.admin import router as admin_router
from db.base import engine, Base
from scheduler import setup_scheduler
from handlers.staff import router as staff_router
from handlers.support import router as support_router

logging.basicConfig(level=logging.ERROR)

async def main():

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(admin_router)
    dp.include_router(support_router)
    dp.include_router(staff_router)
    dp.include_router(router)

    scheduler = setup_scheduler(bot)  
    scheduler.start()   

    print("🤖 Bot is running...")
    await dp.start_polling(bot)



asyncio.run(main())
