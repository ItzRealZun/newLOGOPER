from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import handlers.keyboards as kb

class Auth(StatesGroup):
    id = State()


manager_router: Router = Router()

@manager_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Auth.id)
    await message.answer("Введите ваш идентификатор менеджера:")

@manager_router.message(Auth.id)
async def after_auth(message: Message, state: FSMContext) -> None:
    await state.update_data(id=message.text)
    await message.answer("Вы успешно вошли в бота", reply_markup=kb.end_button)
    await state.clear()

"""
@manager_router.callback_query(F.data == "end")
async def cmd_end(callback: CallbackQuery) -> None:
    await callback.message.answer("Спасибо за использование нашего бота!", reply_markup=kb.end_button)
"""