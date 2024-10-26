import asyncio
from os import getenv
from typing import Final
from aiogram import Dispatcher, Bot
from aiogram.utils.token import TokenValidationError
from handlers.user import user_router, auth_router
from handlers.manager import manager_router


async def main(MAIN_ROUTER: Dispatcher, ROUTERS: list) -> None:
    for router in ROUTERS:
        MAIN_ROUTER.include_router(router)
    await MAIN_ROUTER.start_polling(bot)

if __name__ == "__main__":
    try:
        TOKEN: Final[str] = getenv("BOT_TOKEN")
        bot: Bot = Bot(token=TOKEN)
        dp: Dispatcher = Dispatcher()
        asyncio.run(main(dp, [auth_router, user_router]))
    except TokenValidationError:
        print("Invalid token")
    except KeyboardInterrupt:
        print("Exit")
