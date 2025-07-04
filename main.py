import asyncio
from aiogram import Dispatcher, Bot, Router
from aiogram.utils.token import TokenValidationError

from handlers.user import user_router, auth_router
from handlers.manager import manager_router
from handlers.filters import get_managers
from configuration.config import Config, load_config


async def main(main_router: Dispatcher, routers: tuple[Router, ...], bot: Bot, db_config: dict[str, str]) -> None:
    # link all routers to main router (dispatcher)
    for router in routers:
        main_router.include_router(router)
    await main_router.start_polling(bot, 
                                    db_config=db_config, 
                                    bot_var=bot, 
                                    client_manager={m: None for m in get_managers()},
                                    client_db={},
                                    manager_db={})

if __name__ == "__main__":
    # read bot token from environment, create bot instance, run bot
    try:
        config: Config = load_config()
        bot:       Bot = Bot(token=config.tg_bot.token)
        dp: Dispatcher = Dispatcher()
        asyncio.run(main(main_router=dp, 
                        routers=(auth_router, user_router, manager_router), 
                        bot=bot, 
                        db_config=config.db.to_dict()))
    except TokenValidationError:
        print("Invalid token")
    except KeyboardInterrupt:
        print("Exit")
