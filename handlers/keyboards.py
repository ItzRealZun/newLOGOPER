from aiogram.types import ReplyKeyboardMarkup as r_keyboard, KeyboardButton as r_button
from aiogram.types import InlineKeyboardMarkup as i_keyboard, InlineKeyboardButton as i_button

main_menu = i_keyboard(inline_keyboard=[
    [i_button(text="Ответы на частозадаваемые вопросы", callback_data="answers")],
    [i_button(text="Информация по заказу", callback_data="info")],
    [i_button(text="Оценка менеджера", callback_data="mark")],
    [i_button(text="Завершить диалог", callback_data="end")]
])

return_button = i_button(text="Назад", callback_data="end")

end_button = r_keyboard(keyboard=[[r_button(text="/start")]])

rating_menu = i_keyboard(inline_keyboard=[
    [i_button(text="★", callback_data="1")],
    [i_button(text="★★", callback_data="2")],
    [i_button(text="★★★", callback_data="3")],
    [i_button(text="★★★★", callback_data="4")],
    [i_button(text="★★★★★", callback_data="5")],
])
