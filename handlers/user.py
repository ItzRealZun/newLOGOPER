from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import keyboards as kb

class Auth(StatesGroup):
    order_number = State()


user_router: Router = Router()

@user_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await state.set_state(Auth.order_number)
    await message.answer("Введите номер заказа:")

@user_router.message(Auth.order_number)
async def after_auth(message: Message, state: FSMContext) -> None:
    await state.update_data(order_number=message.text)
    await message.answer("Вы успешно вошли в бота", reply_markup=kb.main_menu)
    await state.clear()


@user_router.callback_query(F.data == "end")
async def cmd_end(callback: CallbackQuery) -> None:
    await callback.message.answer("Спасибо за использование нашего бота!", reply_markup=kb.end_button)
