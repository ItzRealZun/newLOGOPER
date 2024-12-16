from aiogram import F, Router, Bot
from aiogram.filters import CommandStart, invert_f, or_f
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message, ReplyKeyboardMarkup, User
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from loguru import logger

import handlers.keyboards as kb
from handlers.filters import is_user
from postgres import Client, IncorrectKey


logger.add(sink="debug.log", format="{time} {message}", level="DEBUG", rotation="100 KB")
photos = {}


def connect_with_manager(dct: dict[int, int | None]) -> int | None:
    # find first free manager to connect
    for key in dct:
        if dct[key] is None:
            return key
    return None


def find_manager_in_dict(value: int, dct: dict[int, int | None]) -> int | None:
    # find connected manager
    for key in dct:
        if dct[key] == value:
            return key
    return None


class Enter(StatesGroup):
    # class to authenticate into a bot by entering unique key of client
    key: State = State()


class Exit(StatesGroup): 
    # class to exit from dialog
    flag: State = State()


class Chat(StatesGroup):
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
user_router.callback_query.filter(invert_f(or_f(Enter.key, Exit.flag)), is_user) 
# block ability to click on buttons when not logined


@auth_router.message(CommandStart())
async def command_start(message: Message, state: FSMContext) -> None:
    # start bot dialog and auth by unique secret key 
    assert isinstance(message.from_user, User)
    logger.debug(f"{message.from_user.id} {message.from_user.first_name}")
    await state.clear()
    await state.set_state(Enter.key)
    stage: kb.Stage = kb.stages["auth"]
    await message.answer(text=stage.text, reply_markup=stage.keyboard)


@user_router.message(Chat.flag)
async def interact_chat(message: Message, state: FSMContext, bot_var: Bot, client_manager: dict) -> None:
    # chat with manager
    result: int | None = find_manager_in_dict(message.chat.id, client_manager)
    if not(result) or message.text == "/stop":
        if result is not None:
            client_manager[result] = None
        await state.clear()
        await message.answer(text="Диалог завершён!")
        stage: kb.Stage = kb.stages["after_chat"]
        await message.answer(text=stage.text, reply_markup=stage.keyboard)
    else:
        assert isinstance(message.text, str)
        await bot_var.send_message(chat_id=result, text=message.text)


@auth_router.message(Enter.key)
async def after_auth(message: Message, state: FSMContext, db_config, client_db) -> None:
    # finish auth and display main menu
    assert isinstance(message.from_user, User) and isinstance(message.text, str)
    try:
        client_obj = Client(db_config, message.text)
        client_db[message.from_user.id] = client_obj
        stage: kb.Stage = kb.create_main_menu_stage(client_obj.greeting())
        await message.answer(text=stage.text, reply_markup=stage.keyboard)
        await state.clear()
    except IncorrectKey:
        await message.answer(text="Неверный токен. Попробуйте ещё раз")


@user_router.callback_query(F.data == "menu")
async def goto_menu(callback: CallbackQuery) -> None:
    # return to main menu 
    assert isinstance(callback.message, Message)
    stage: kb.Stage = kb.stages["main_menu"]
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)
    

@user_router.callback_query(F.data == "contacts")
async def goto_contacts(callback: CallbackQuery) -> None:
    # list LOGOPER contacts
    assert isinstance(callback.message, Message)
    stage: kb.Stage = kb.stages["contacts"]
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)


@user_router.callback_query(F.data.in_({"MOSKVA", "SANKTPETERBURG", "NAHODKA", "NOVOSIBIRSK", "VLADIVOSTOK", "KRASNOYARSK", "EKATERINBURG"}))
async def goto_city(callback: CallbackQuery) -> None:
    # list cities where LOGOPER is located
    assert isinstance(callback.message, Message) and isinstance(callback.data, str)
    stage: kb.Stage = kb.stages[callback.data]
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)


@user_router.callback_query(F.data == "geography")
async def goto_geography(callback: CallbackQuery, bot_var: Bot) -> None:
    # list geography cart
    assert isinstance(callback.message, Message)
    global photos
    if photos.get(callback.from_user.id) is None:
        msg = await bot_var.send_photo(chat_id=callback.from_user.id, photo="AgACAgIAAxkBAAIK4WdgO_EjGmlaMz5oozeJN_y72AaGAAJI6jEbCKwISzA3oOcaWXrHAQADAgADeQADNgQ")
        photos[callback.from_user.id] = msg.message_id
    stage: kb.Stage = kb.stages["geography"]
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)


@user_router.callback_query(F.data == "info")
async def goto_answers(callback: CallbackQuery, bot_var: Bot) -> None:
    # list available information about LOGOPER
    assert isinstance(callback.message, Message)
    global photos
    if x := photos.get(callback.from_user.id):
        await bot_var.delete_message(callback.from_user.id, x)
        del photos[callback.from_user.id]
    stage: kb.Stage = kb.stages["info"]
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)


@user_router.callback_query(F.data == "orders")
async def goto_orders_list(callback: CallbackQuery, client_db) -> None:
    # list client's orders
    assert isinstance(callback.message, Message)
    stage: kb.Stage = kb.create_selecting_order_stage(client_db[callback.from_user.id].cargos_small())
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)

    
@user_router.callback_query(F.data == "end")
async def command_end(callback: CallbackQuery, state: FSMContext) -> None:
    # finish bot dialog
    assert isinstance(callback.message, Message)
    stage: kb.Stage = kb.stages["end"]
    assert isinstance(stage.keyboard, ReplyKeyboardMarkup)
    await state.set_state(Exit.flag)
    await callback.message.answer(text=stage.text, reply_markup=stage.keyboard)
 

@user_router.callback_query(lambda cb: cb.data.startswith("order_"))
async def goto_order(callback: CallbackQuery, client_db) -> None:
    # list information about selected order 
    assert isinstance(callback.message, Message) and isinstance(callback.data, str)
    number = int(callback.data.replace("order_", ''))
    stage: kb.Stage = kb.create_order_stage(client_db[callback.from_user.id].cargo_detailed(number))
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)


@user_router.callback_query(F.data == "chat")
async def goto_chat(callback: CallbackQuery, state: FSMContext, bot_var: Bot, client_manager: dict) -> None:
    # await manager's answer 
    assert isinstance(callback.message, Message) and isinstance(callback.message.from_user, User)
    stage: kb.Stage = kb.stages["chat"]
    await callback.message.edit_text(text=stage.text)
    result: int | None = connect_with_manager(client_manager)
    if result:
        client_manager[result] = callback.message.chat.id 
        await bot_var.send_message(chat_id=result, text="Поступил запрос на диалог с менеджером")
        await state.set_state(Chat.flag)
    else:
        await bot_var.send_message(chat_id=callback.message.chat.id, text="Не удалось найти свободного менеджера")
        stage: kb.Stage = kb.stages["after_chat"]
        await callback.message.answer(text=stage.text, reply_markup=stage.keyboard)


@user_router.callback_query(F.data == "rate")
async def goto_marking(callback: CallbackQuery, state: FSMContext) -> None:
    # first step of marking manager
    assert isinstance(callback.message, Message) 
    await state.set_state(Marking.quality_of_service)
    stage: kb.Stage = kb.create_rating_stage("качество обслуживания")
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)


@user_router.callback_query(F.data.in_("12345") and Marking.quality_of_service)
async def marking_first_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # second step of marking manager
    assert isinstance(callback.message, Message) and isinstance(callback.data, str)
    await state.update_data(quality_of_service=int(callback.data))
    await state.set_state(Marking.communication_efficiency)
    stage: kb.Stage = kb.create_rating_stage("эффективность коммуникации")
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)
    

@user_router.callback_query(F.data.in_("12345") and Marking.communication_efficiency)
async def marking_second_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # third step of marking manager
    assert isinstance(callback.message, Message) and isinstance(callback.data, str) 
    await state.update_data(communication_efficiency=int(callback.data))
    await state.set_state(Marking.professionalism_level)
    stage: kb.Stage = kb.create_rating_stage("уровень профессионализма")
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)
    

@user_router.callback_query(F.data.in_("12345") and Marking.professionalism_level)
async def marking_third_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # fourth step of marking manager
    assert isinstance(callback.message, Message) and isinstance(callback.data, str) 
    await state.update_data(professionalism_level=int(callback.data))
    await state.set_state(Marking.ability_of_problem_solving)
    stage: kb.Stage = kb.create_rating_stage("способность решать проблемы")
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)


@user_router.callback_query(F.data.in_("12345") and Marking.ability_of_problem_solving)
async def marking_fourth_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # fifth step of marking manager
    assert isinstance(callback.message, Message) and isinstance(callback.data, str) 
    await state.update_data(ability_of_problem_solving=int(callback.data))
    await state.set_state(Marking.speed_of_work)
    stage: kb.Stage = kb.create_rating_stage("скорость работы")
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)
    

@user_router.callback_query(F.data.in_("12345") and Marking.speed_of_work)
async def marking_fifth_ended(callback: CallbackQuery, state: FSMContext) -> None:
    # end of marking manager
    assert isinstance(callback.message, Message) and isinstance(callback.data, str) 
    await state.update_data(speed_of_work=int(callback.data))
    await state.clear()
    stage: kb.Stage = kb.stages["after_rate"]
    assert isinstance(stage.keyboard, InlineKeyboardMarkup)
    await callback.message.edit_text(text=stage.text, reply_markup=stage.keyboard)
