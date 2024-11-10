from aiogram import F, Router
from aiogram.filters import CommandStart, invert_f, or_f
from aiogram.types import CallbackQuery, Message, User
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from loguru import logger

import handlers.keyboards as kb
from handlers.lexicon import text_lexicon, marking_lexicon
from handlers.filters import is_user 


logger.add(sink="debug.log", format="{time} {message}", level="DEBUG", rotation="100 KB")


class Enter(StatesGroup):
    # class to authenticate into a bot by entering order number of client
    order_number: State = State()


class Exit(StatesGroup): # class to exit from dialog
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

auth_router.message.filter(is_user) # filter only users
user_router.message.filter(is_user) # filter only users
user_router.callback_query.filter(invert_f(or_f(Enter.order_number, Exit.flag)), is_user) 
# block ability to click on buttons when not logined


@auth_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    # start bot dialog and auth by order number
    assert isinstance(message.from_user, User)
    logger.debug(f"{message.from_user.id} {message.from_user.first_name}")
    await state.clear()
    await state.set_state(Enter.order_number)
    await message.answer(text_lexicon["start"], 
                        reply_markup=kb.remove)


@auth_router.message(Enter.order_number)
async def after_auth(message: Message, state: FSMContext) -> None:
    # finish auth and display main menu
    await state.update_data(order_number=message.text)
    await message.answer("Здравствуйте, {name}!. Выберите необходимый пункт меню:", 
                        reply_markup=kb.main_menu)
    await state.clear()


@user_router.callback_query(F.data == "menu")
async def goto_menu(callback: CallbackQuery) -> None:
    # return to main menu 
    assert isinstance(callback.message, Message) 
    await callback.message.edit_text(text_lexicon["menu"], 
                                    reply_markup=kb.main_menu)


@user_router.callback_query(F.data == "answers")
async def goto_answers(callback: CallbackQuery) -> None:
    # list questions and their answers
    assert isinstance(callback.message, Message) and isinstance(callback.data, str) 
    await callback.message.edit_text(text_lexicon["answers"],
                                     reply_markup=kb.answers_menu)


@user_router.callback_query(F.data.in_({"info", "chat"}))
async def goto_info_or_chat(callback: CallbackQuery) -> None:
    # list selected info
    assert isinstance(callback.message, Message) and isinstance(callback.data, str) 
    await callback.message.edit_text(text_lexicon[callback.data],
                                    reply_markup=kb.return_menu)


@user_router.callback_query(F.data == "end")
async def command_end(callback: CallbackQuery, state: FSMContext) -> None:
    # finish bot dialog
    assert isinstance(callback.message, Message) 
    await state.set_state(Exit.flag)
    await callback.message.answer(text_lexicon["end"], 
                                reply_markup=kb.end_menu)
    

@user_router.callback_query(F.data == "mark")
async def goto_marking(callback: CallbackQuery, state: FSMContext) -> None:
    # first step of marking manager
    assert isinstance(callback.message, Message) 
    await state.set_state(Marking.quality_of_service)
    await callback.message.edit_text(marking_lexicon[0], 
                                    reply_markup=kb.rating_menu)


@user_router.callback_query(F.data.in_("12345") and Marking.quality_of_service)
async def marking_first_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # second step of marking manager
    assert isinstance(callback.message, Message) and isinstance(callback.data, str)
    await state.update_data(quality_of_service=int(callback.data))
    await state.set_state(Marking.communication_efficiency)
    await callback.message.edit_text(marking_lexicon[1], 
                                    reply_markup=kb.rating_menu)


@user_router.callback_query(F.data.in_("12345") and Marking.communication_efficiency)
async def marking_second_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # third step of marking manager
    assert isinstance(callback.message, Message) and isinstance(callback.data, str) 
    await state.update_data(communication_efficiency=int(callback.data))
    await state.set_state(Marking.professionalism_level)
    await callback.message.edit_text(marking_lexicon[2], 
                                    reply_markup=kb.rating_menu)


@user_router.callback_query(F.data.in_("12345") and Marking.professionalism_level)
async def marking_third_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # fourth step of marking manager
    assert isinstance(callback.message, Message) and isinstance(callback.data, str) 
    await state.update_data(professionalism_level=int(callback.data))
    await state.set_state(Marking.ability_of_problem_solving)
    await callback.message.edit_text(marking_lexicon[3], 
                                    reply_markup=kb.rating_menu)


@user_router.callback_query(F.data.in_("12345") and Marking.ability_of_problem_solving)
async def marking_fourth_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # fifth step of marking manager
    assert isinstance(callback.message, Message) and isinstance(callback.data, str) 
    await state.update_data(ability_of_problem_solving=int(callback.data))
    await state.set_state(Marking.speed_of_work)
    await callback.message.edit_text(marking_lexicon[4], 
                                    reply_markup=kb.rating_menu)



@user_router.callback_query(F.data.in_("12345") and Marking.speed_of_work)
async def marking_fifth_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # end of marking manager
    assert isinstance(callback.message, Message) and isinstance(callback.data, str) 
    await state.update_data(speed_of_work=int(callback.data))
    await state.clear()
    await callback.message.edit_text(text_lexicon["thanks"], 
                                    reply_markup=kb.return_menu)
