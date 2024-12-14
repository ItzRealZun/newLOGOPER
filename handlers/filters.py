from aiogram.types import Message, User
import json


def get_managers() -> list[int]:
    with open(file="handlers/telegram_managers.json", mode="rt", encoding="utf-8") as file:
        return json.load(fp=file)


def is_manager(message: Message) -> bool: 
    assert isinstance(message.from_user, User)
    return message.from_user.id in get_managers()


def is_user(message: Message) -> bool:
    return not is_manager(message)
