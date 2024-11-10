from aiogram.types import ReplyKeyboardMarkup as r_keyboard, KeyboardButton as r_button
from aiogram.types import InlineKeyboardMarkup as i_keyboard, InlineKeyboardButton as i_button
from aiogram.types import ReplyKeyboardRemove as no_keyboard

from handlers.lexicon import answers_menu_lexicon, main_menu_lexicon

remove: no_keyboard = no_keyboard()

answers_menu: i_keyboard = i_keyboard(inline_keyboard=[[i_button(text=value, callback_data=key)] 
                                                for key, value in answers_menu_lexicon.items()])

main_menu: i_keyboard = i_keyboard(inline_keyboard=[[i_button(text=value, callback_data=key)] 
                                                for key, value in main_menu_lexicon.items()])

return_menu: i_keyboard = i_keyboard(inline_keyboard=[[i_button(text="Главное меню", callback_data="menu")]])

end_menu: r_keyboard = r_keyboard(keyboard=[[r_button(text="/start")]], resize_keyboard=True)

rating_menu: i_keyboard = i_keyboard(inline_keyboard=[[i_button(text="★" * i, callback_data=str(i))] 
                                                    for i in range(1, 6)])
