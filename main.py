import asyncio
from os import getenv
from typing import Final
from aiogram import Dispatcher, Bot
from handlers import router

TOKEN: Final[str] = getenv("BOT_TOKEN")

bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher()

async def main() -> None:
    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Exit")
