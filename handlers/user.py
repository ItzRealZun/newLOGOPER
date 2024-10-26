from aiogram import F, Router
from aiogram.filters import CommandStart, Command, invert_f, or_f
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import handlers.keyboards as kb


class Enter(StatesGroup):
    # class to authenticate into a bot by entering order number of client
    order_number: State = State()


class Exit(StatesGroup):
    # class to exit from dialog
    flag: State = State()


class Marking(StatesGroup):
    # class to mark a manager who is connected to order number of client
    quality_of_service:         State = State()
    communication_efficiency:   State = State()
    professionalism_level:      State = State()
    ability_of_problem_solving: State = State()
    speed_of_work:              State = State()


auth_router: Router = Router() # router for entering and exiting events
user_router: Router = Router() # router for events on user-side
user_router.callback_query.filter(invert_f(or_f(Enter.order_number, Exit.flag))) 
# cannot click on buttons when not logined


criteria: tuple[str, ...] = ('Оцените качество обслуживания', 'Оцените эффективность коммуникации', 
        'Оцените уровень профессионализма', 'Оцените способность решать проблемы', 'Оцените скорость работы')


@auth_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    # start bot dialog and auth by order number
    with open(file="users.txt", mode="a", encoding="utf-8") as file:
        file.write(f"{message.date.strftime("%d.%m.%Y %H:%M")} | {message.from_user.id} {message.from_user.first_name}\n")
    await state.clear()
    await state.set_state(Enter.order_number)
    await message.answer("Введите номер заказа для входа в бота:", 
                        reply_markup=kb.remove)


@auth_router.message(Enter.order_number)
async def after_auth(message: Message, state: FSMContext) -> None:
    # finish auth and display main menu
    await state.update_data(order_number=message.text)
    await message.answer("Вы успешно вошли в бота. Выберите необходимый пункт меню:", 
                        reply_markup=kb.main_menu)
    await state.clear()


@user_router.callback_query(F.data == "menu")
async def goto_menu(callback: CallbackQuery) -> None:
    # return to main menu
    await callback.message.edit_text(f"Выберите необходимый пункт меню:", 
                                    reply_markup=kb.main_menu)


@user_router.callback_query(F.data == "answers")
async def goto_answers(callback: CallbackQuery) -> None:
    # list most frequently asked questions
    with open(file="questions.txt", mode="rt", encoding="utf-8") as file:
        await callback.message.edit_text("Список частозадаваемых вопросов:\n" + file.read(), 
                                        reply_markup=kb.return_menu)


@user_router.callback_query(F.data == "info")
async def goto_info(callback: CallbackQuery) -> None:
    # list information about order
    await callback.message.edit_text("Информация по заказу:", 
                                    reply_markup=kb.return_menu)


@user_router.callback_query(F.data == "end")
async def command_end(callback: CallbackQuery, state: FSMContext) -> None:
    # finish bot dialog
    await state.set_state(Exit.flag)
    await callback.message.answer("Спасибо за использование нашего бота!", 
                                reply_markup=kb.end_menu)
    

@user_router.callback_query(F.data == "mark")
async def goto_marking(callback: CallbackQuery, state: FSMContext) -> None:
    # first step of marking manager
    await state.set_state(Marking.quality_of_service)
    await callback.message.edit_text(criteria[0], 
                                    reply_markup=kb.rating_menu)


@user_router.callback_query(F.data.in_("12345") and Marking.quality_of_service)
async def marking_first_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # second step of marking manager
    await state.update_data(quality_of_service=int(callback.data))
    await state.set_state(Marking.communication_efficiency)
    await callback.message.edit_text(criteria[1], 
                                    reply_markup=kb.rating_menu)


@user_router.callback_query(F.data.in_("12345") and Marking.communication_efficiency)
async def marking_second_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # third step of marking manager
    await state.update_data(communication_efficiency=int(callback.data))
    await state.set_state(Marking.professionalism_level)
    await callback.message.edit_text(criteria[2], 
                                    reply_markup=kb.rating_menu)


@user_router.callback_query(F.data.in_("12345") and Marking.professionalism_level)
async def marking_third_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # fourth step of marking manager
    await state.update_data(professionalism_level=int(callback.data))
    await state.set_state(Marking.ability_of_problem_solving)
    await callback.message.edit_text(criteria[3], 
                                    reply_markup=kb.rating_menu)


@user_router.callback_query(F.data.in_("12345") and Marking.ability_of_problem_solving)
async def marking_fourth_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # fifth step of marking manager
    await state.update_data(ability_of_problem_solving=int(callback.data))
    await state.set_state(Marking.speed_of_work)
    await callback.message.edit_text(criteria[4], 
                                    reply_markup=kb.rating_menu)


@user_router.callback_query(F.data.in_("12345") and Marking.speed_of_work)
async def marking_fifth_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # end of marking manager
    await state.update_data(speed_of_work=int(callback.data))
    await state.clear()
    await callback.message.edit_text("Благодарим за Вашу оценку!", 
                                    reply_markup=kb.return_menu)