from dataclasses import dataclass
from psycopg2 import connect

class IncorrectKey(Exception): ...


def execute_select_command(command: str, config: dict[str, str]) -> list[tuple]:
    with connect(dbname=config["database"], host=config["db_host"], user=config["db_user"], 
                 password=config["db_password"], port=config["db_port"]) as conn:
        with conn.cursor() as cursor:
            cursor.execute(command)
            return cursor.fetchall()


def execute_rating(config: dict[str, str], rates: tuple[int, int, int, int, int], client_id: int, manager_id: int) -> None:
    with connect(dbname=config["database"], host=config["db_host"], user=config["db_user"], 
                 password=config["db_password"], port=config["db_port"]) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'INSERT INTO public."marks" VALUES ((SELECT mark_id FROM public."marks" ORDER BY mark_id DESC LIMIT 1) + 1, {rates[0]}, {rates[1]}, {rates[2]}, {rates[3]}, {rates[4]}, {client_id}, {manager_id})')
            conn.commit()


@dataclass
class Client:
    @classmethod
    def get_client_row(cls, db_config: dict[str, str], secret_key: str) -> tuple | None:
        command: str = f'SELECT * FROM public."clients" WHERE secret_key=\'{secret_key}\''
        result: list[tuple] = execute_select_command(command, db_config)
        if result:
            return result[0]
        return None


    @classmethod
    def get_client_cargos(cls, db_config: dict[str, str], client_id: int) -> list[tuple]:
        command: str = f'SELECT * FROM public."client_cargo" JOIN public."cargos" ON public."cargos".cargo_id = public."client_cargo".cargo_id WHERE public."client_cargo".client_id={client_id}'
        result: list[tuple] = execute_select_command(command, db_config)
        return [line[3:] for line in result]


    def __init__(self, db_config: dict[str, str], secret_key: str) -> None:
        result: tuple | None = Client.get_client_row(db_config, secret_key)
        if result:
            self.__client_id, self.__surname, self.__name, self.__last_name, self.__email, self.__secret_key, self.__company = result
            self.__client_id: int = int(self.__client_id)
            self.__cargos: list[tuple] = Client.get_client_cargos(db_config, self.__client_id)
        else:
            raise IncorrectKey("Secret key is not valid")


    def __repr__(self) -> str:
        return f"""Client({self.__client_id}, 
                            {self.__surname}, 
                            {self.__name}, 
                            {self.__last_name}, 
                            {self.__email}, 
                            {self.__secret_key},  
                            {self.__company})"""


    def greeting(self) -> str:
        middle = "ая" if self.__last_name[-1] == 'а' else "ый"
        return f"Здравствуйте, уважаем{middle} {self.__name} {self.__last_name}! Выберите необходимый пункт меню:"

    
    def cargo_detailed(self, number: int) -> tuple:
        return self.__cargos[number - 1]


    def cargos_small(self) -> list[tuple[str, int]]:
        return [(f"Заказ {index} ({cargo[2]})", index) for index, cargo in enumerate(self.__cargos, 1)]


    @classmethod
    def answers(cls, db_config: dict[str, str]) -> list[tuple]:
        command: str = 'SELECT * FROM public."questions"'
        return execute_select_command(command, db_config)
