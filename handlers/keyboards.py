from dataclasses import dataclass
from aiogram.types import ReplyKeyboardMarkup as r_keyboard, KeyboardButton as r_button
from aiogram.types import InlineKeyboardMarkup as i_keyboard, InlineKeyboardButton as i_button
from aiogram.types import ReplyKeyboardRemove as empty_keyboard
from typing import Final


def get_questions(path: str) -> str:
    with open(file=path, mode="rt", encoding="utf-8") as file:
        return file.read()


@dataclass
class Stage: 
    text: str 
    keyboard: i_keyboard | r_keyboard | empty_keyboard

def create_return_button(source: str) -> i_button:
    return i_button(text="Назад", callback_data=source)


buttons: Final[dict[str, i_button]] = {
    "return_button":         i_button(text="Назад", callback_data="return"),
    "main_menu_button":      i_button(text="Главное меню", callback_data="menu"),
    "manager_rating_button": i_button(text="Оценить менеджера", callback_data="rate"),
    "orders_list_button":    i_button(text="Мои заказы", callback_data="orders"),
    "end_dialog_button":     i_button(text="Завершить диалог", callback_data="end"),
    "info_button":           i_button(text="Общая информация", callback_data="info"),
    "ask_chat_button":       i_button(text="Запросить диалог с менеджером", callback_data="chat"),
    "contacts_button":       i_button(text="Контакты", callback_data="contacts"),
    "geography_button":      i_button(text="География перевозок", callback_data="geography"),
    "MOSKVA":                i_button(text="Москва", callback_data="MOSKVA"),
    "SANKTPETERBURG":        i_button(text="Санкт-Петербург", callback_data="SANKTPETERBURG"),
    "NAHODKA":               i_button(text="Находка", callback_data="NAHODKA"),
    "NOVOSIBIRSK":           i_button(text="Новосибирск", callback_data="NOVOSIBIRSK"),
    "VLADIVOSTOK":           i_button(text="Владивосток", callback_data="VLADIVOSTOK"),
    "KRASNOYARSK":           i_button(text="Красноярск", callback_data="KRASNOYARSK"),
    "EKATERINBURG":          i_button(text="Екатеринбург", callback_data="EKATERINBURG"),
}

stages: Final[dict[str, Stage]] = {
    "auth":            Stage("Введите ключ из личного кабинета для входа в бота:", 
                             empty_keyboard()),

    "main_menu":       Stage("Выберите необходимый пункт меню:", 
                             i_keyboard(inline_keyboard=[[buttons["info_button"]], 
                                                         [buttons["orders_list_button"]], 
                                                         [buttons["end_dialog_button"]]])),

    "info":            Stage("Выберите необходимый пункт меню:", 
                             i_keyboard(inline_keyboard=[[buttons["contacts_button"]],
                                                         [buttons["geography_button"]],
                                                         [create_return_button("menu")]])),

    "chat":            Stage("Скоро с вами свяжется менеджер. Для завершения диалога напишите /stop",
                             empty_keyboard()),

    "after_chat":      Stage("Выберите необходимый пункт меню:",
                             i_keyboard(inline_keyboard=[[buttons["manager_rating_button"]],
                                                         [buttons["main_menu_button"]]])),

    "end":             Stage("Спасибо за использование нашего бота!\nЧтобы снова воспользоваться ботом, нажмите на кнопку:",
                             r_keyboard(keyboard=[[r_button(text="/start")]], resize_keyboard=True)),

    "after_rate":      Stage("Благодарим за Вашу оценку!",
                             i_keyboard(inline_keyboard=[[buttons["main_menu_button"]]])),

    "contacts":        Stage("Выберите город:",
                             i_keyboard(inline_keyboard=[[buttons["MOSKVA"]],
                                                         [buttons["SANKTPETERBURG"]],
                                                         [buttons["NAHODKA"]],
                                                         [buttons["NOVOSIBIRSK"]],
                                                         [buttons["VLADIVOSTOK"]],
                                                         [buttons["KRASNOYARSK"]],
                                                         [buttons["EKATERINBURG"]],
                                                         [create_return_button("info")]])),

    "MOSKVA":          Stage("Контакты ЛОГОПЕР по городу Москва:\nАдрес: Самарская улица 1, БЦ Новион, 4 этаж\nФакс: +74996734210\nРежим работы: пн-чт: 09:00-18:00, пт: 09:00-16:45\nТелефон: +74958704211, +74958704213\nEmail: sale@logoper.ru", 
                             i_keyboard(inline_keyboard=[[create_return_button("contacts")]])),

    "SANKTPETERBURG":  Stage("Контакты ЛОГОПЕР по городу Санкт-Петербург:\nАдрес: ул. Проспект Стачек, 48, офис 109\nРежим работы: пн-чт: 09:00–18:00, пт: 09:00–16:45\nТелефон: +78122197570\nEmail: sale@logoper.ru", 
                             i_keyboard(inline_keyboard=[[create_return_button("contacts")]])),

    "NAHODKA":         Stage("Контакты ЛОГОПЕР по городу Находка:\nАдрес: Шоссейная 118А, оф.11\nРежим работы: пн-чт: 09:00–18:00, пт: 09:00–16:45\nТелефон: +79140726816, +79804097783\nEmail: sale@logoper.ru", 
                             i_keyboard(inline_keyboard=[[create_return_button("contacts")]])),

    "NOVOSIBIRSK":     Stage("Контакты ЛОГОПЕР по городу Новосибирск:\nАдрес: ул. Трудовая, 5\nРежим работы: пн-чт: 09:00–18:00, пт: 09:00–16:45\nТелефон: +73832095410\nEmail: sale@logoper.ru",
                             i_keyboard(inline_keyboard=[[create_return_button("contacts")]])),

    "VLADIVOSTOK":     Stage("Контакты ЛОГОПЕР по городу Владивосток:\nАдрес: ул. Пушкинская, 40, офис 1103-1106\nРежим работы: пн-чт: 09:00–18:00, пт: 09:00–16:45\nТелефон: +74232783450\nEmail: Com-vvo@logoper.ru",
                             i_keyboard(inline_keyboard=[[create_return_button("contacts")]])),

    "KRASNOYARSK":     Stage("Контакты ЛОГОПЕР по городу Красноярск:\nАдрес: ул. Брянская 142, офис 5-20\nРежим работы: пн-чт: 09:00–18:00, пт: 09:00–16:45\nТелефон: +74958704211\nEmail: logoper-krsk@logoper.ru", 
                             i_keyboard(inline_keyboard=[[create_return_button("contacts")]])),

    "EKATERINBURG":    Stage("Контакты ЛОГОПЕР по городу Екатеринбург:\nАдрес: ул. Розы Люксембург, 22, офис 714\nРежим работы: пн-чт: 09:00–18:00, пт: 09:00–16:45\nТелефон: +73432287099\nEmail: sale@logoper.ru",
                             i_keyboard(inline_keyboard=[[create_return_button("contacts")]])),

    "geography":       Stage("География наших перевозок на картинке ниже", 
                             i_keyboard(inline_keyboard=[[create_return_button("info")]]))
}

def create_rating_stage(parameter: str) -> Stage:
    return Stage(f"Оцените {parameter}", 
                 i_keyboard(inline_keyboard=[[i_button(text="★" * i, 
                                                       callback_data=str(i))] 
                                            for i in range(1, 6)]))


def create_main_menu_stage(greeting: str) -> Stage:
    return Stage(greeting, i_keyboard(inline_keyboard=[[buttons["info_button"]], 
                                                       [buttons["orders_list_button"]], 
                                                       [buttons["end_dialog_button"]]]))


def create_selecting_order_stage(lines: list[tuple]) -> Stage:
    buttons = [[i_button(text=line[0], callback_data=f"order_{line[1]}")] for line in lines] 
    return Stage("Ваши заказы:", 
                 i_keyboard(inline_keyboard=buttons+[[create_return_button("menu")]]))


def create_order_stage(line: tuple) -> Stage:
    return Stage(f"Заказ ({line[2]})\nТип перевозки: {line[3]}\nКол-во контейнеров: {line[4]}\nВид контейнера: {line[5]} футов\nМаршрут: {line[6]} - {line[7]}\nВес груза: {line[8]}\nПеревозка завершена: {line[9]}\nСодержимое груза: {line[10]}\nКол-во мест: {line[11]}\n□ - Морское плечо\n□ - Ж/Д плечо\n□ - Транспортировка до терминала\n■ - Последние мили",
                 i_keyboard(inline_keyboard=[[buttons["ask_chat_button"]], 
                                             [create_return_button("orders")]]))
