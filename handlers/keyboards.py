from aiogram.types import ReplyKeyboardMarkup as r_keyboard, KeyboardButton as r_button
from aiogram.types import InlineKeyboardMarkup as i_keyboard, InlineKeyboardButton as i_button
from aiogram.types import ReplyKeyboardRemove as no_keyboard

remove: no_keyboard = no_keyboard()

main_menu: i_keyboard = i_keyboard(inline_keyboard=[
    [i_button(text="Ответы на частозадаваемые вопросы", callback_data="answers")],
    [i_button(text="Информация по заказу", callback_data="info")],
    [i_button(text="Оценка менеджера", callback_data="mark")],
    [i_button(text="Завершить диалог", callback_data="end")]
])

return_menu: i_keyboard = i_keyboard(inline_keyboard=[[i_button(text="Главное меню", callback_data="menu")]])

end_menu: r_keyboard = r_keyboard(keyboard=[[r_button(text="/start")]], resize_keyboard=True)

rating_menu: i_keyboard = i_keyboard(inline_keyboard=[
    [i_button(text="★" * i, callback_data=str(i))] for i in range(1, 6)
])