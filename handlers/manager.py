from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters import Command

from handlers.filters import is_manager


manager_router: Router = Router()
manager_router.message.filter(is_manager) # filter only managers

@manager_router.message(Command("stop"))
async def stop_chat(message: Message, bot_var: Bot, client_manager: dict[int, int | None]) -> None:
    # stop chat with client
    result: int | None = client_manager[message.chat.id]
    if result:
        client_manager[message.chat.id] = None
        await bot_var.send_message(chat_id=result, text="Диалог завершён!")
    else:
        await message.answer(text="Нет активного диалога с клиентом")
        

@manager_router.message()
async def send_answer(message: Message, bot_var: Bot, client_manager: dict) -> None:
    # chat with client
    result: int | None = client_manager[message.chat.id]
    if result:
        assert isinstance(message.text, str)
        await bot_var.send_message(chat_id=result, text=message.text)
    else:
        await message.answer(text="Нет активного диалога с клиентом")
