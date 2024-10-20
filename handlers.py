from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, Message

import keyboards as kb

router: Router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer("Вы успешно вошли в бота!", reply_markup=kb.main_menu)

@router.callback_query(F.data == "end")
async def cmd_end(callback: CallbackQuery) -> None:
    await callback.message.answer("Спасибо за использование нашего бота!", reply_markup=kb.end_button)
