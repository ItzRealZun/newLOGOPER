from dataclasses import dataclass
from typing import Any
from psycopg2 import connect
from psycopg2.extensions import connection as Connection, cursor as Cursor


class IncorrectToken(Exception): ...


@dataclass
class PostgresUser:
    role: str
    id: int
    phone_number: str | None
    token: str
    name: str
    last_name: str
    surname: str | None
    male: str

    def __str__(self) -> str:
        return (f"{self.role}: |TOKEN={self.token}, ID={self.id}, PHONE NUMBER={self.phone_number}," 
        f"NAME={self.name}, LAST NAME={self.last_name}, SURNAME={self.surname}, MALE={self.male}|")


class Postgres:
    connection: Connection = connect(dbname="logoper_test", host="emiit.ru", 
                                     user="user1", password="0022", port="5432")
    cursor: Cursor = connection.cursor()

    def __init__(self, token: str) -> None:
        if Postgres.__is_valid_token(token):
            role: str = Postgres.__get_role(token)
            info: tuple[Any, ...] = Postgres.__get_info(token, role)
            if role == "Admins":
                self.__postgres_user: PostgresUser = PostgresUser(role, info[0], None, token, 
                                                                  info[2], info[3], None, info[4])
            else:
                self.__postgres_user: PostgresUser = PostgresUser(role, info[0], info[1], token, 
                                                                  info[3], info[4], info[5], info[6])
        else:
            raise IncorrectToken("This token is invalid!")

    @classmethod
    def __get_info(cls, user_token: str, role: str) -> tuple[Any, ...]:
        """user_token must be valid token from database"""
        cls.cursor.execute(f'SELECT * FROM public."{role}" WHERE token=%s', (user_token, ))
        return cls.cursor.fetchone() or ()

    @classmethod
    def __get_role(cls, user_token: str) -> str:
        """user_token must be valid token from database"""
        cls.cursor.execute('SELECT admin_id FROM public."Admins" WHERE token=%s', (user_token, ))
        return ("Admins" if cls.cursor.fetchone() else "Clients")

    @classmethod
    def __is_valid_token(cls, token: str) -> bool:
        cls.cursor.execute("""SELECT admin_id FROM public."Admins" WHERE token=%s 
                            UNION SELECT client_id FROM public."Clients" WHERE token=%s""", (token, token))
        return bool(cls.cursor.fetchone())
    
    @property
    def postgres_user(self):
        return self.__postgres_user

    def __str__(self) -> str:
        return str(self.__postgres_user)


def main() -> None:
    token = input("Enter token: ")
    my_user = Postgres(token)
    print(my_user)

if __name__ == "__main__":
    main()


"""
class User:
    def __init__(self, chat_id) -> None:
        self.__flag: bool = False
        self.__chat_id = chat_id
        self.__token: int = 0
        self.__managers: list[str] = []
        self.__marking_manager: str = ""
        self.__stage: int = 0

    @property
    def flag(self) -> bool:
        return self.__flag

    @flag.setter
    def flag(self, new_value: bool) -> None:
        self.__flag: bool = new_value


def is_real_number(string: str) -> bool:
    try:
        float(string)
        return True
    except:
        return False


def determine_role(user_token: int) -> str:
    cursor.execute('SELECT * FROM public."Admins" WHERE token=%s', (user_token,))
    if len(cursor.fetchall()) > 0:
        return "Admins"
    cursor.execute('SELECT * FROM public."Clients" WHERE token=%s', (user_token,))
    if len(cursor.fetchall()) > 0:
        return "Clients"
    return "None"


def determine_male(token: str) -> str:
    cursor.execute('SELECT male FROM public."Admins" WHERE token=%s', (token,))
    temp = cursor.fetchall()
    if len(temp) > 0:
        return temp[0][0]
    cursor.execute('SELECT male FROM public."Clients" WHERE token=%s', (token,))
    temp = cursor.fetchall()
    return temp[0][0]


def get_managers(token):
    cursor.execute('SELECT public."Managers".last_name, public."Managers".name, public."Managers".father_name ' +
                   'FROM public."Managers" ' +
                   'JOIN public."Client_Manager" ON public."Managers".manager_id = public."Client_Manager".manager_id' +
                   ' JOIN public."Clients" ON public."Client_Manager".client_id = public."Clients".client_id ' +
                   'WHERE public."Clients".token = %s', (token, ))
    temp = cursor.fetchall()
    if len(temp) > 0:
        for i in range(len(temp)):
            temp[i] = temp[i][0] + " " + temp[i][1][0] + "." + temp[i][2][0] + "."
        return temp
    return "К Вам не прикреплён ни один менеджер"


def refresh_marks(answers, manager):
    cursor.execute('SELECT quality, communication, proff, invent, speed, marks' +
                   ' FROM public."Managers"' +
                   ' WHERE last_name = %s', (list(manager.split())[0], ))
    data = cursor.fetchall()[0]
    marks = data[-1]
    new_marks = [round(((float(data[i]) * marks) + answers[i]) / (marks + 1), 2) for i in range(5)]
    cursor.execute('UPDATE public."Managers"' +
                   ' SET quality=%s, communication=%s, proff=%s, invent=%s, speed=%s, marks=%s' +
                   ' WHERE last_name=%s', (*new_marks, marks + 1, list(manager.split())[0]))
    connection.commit()


def get_stat():
    cursor.execute('SELECT last_name, name, father_name, quality, communication,' +
                   ' proff, invent, speed FROM public."Managers"')
    data = cursor.fetchall()
    if len(data) > 0:
        temp = ""
        for i in range(len(data)):
            sr = round((data[i][3] + data[i][4] + data[i][5] + data[i][6] + data[i][7]) / 5, 2)
            temp += (f'{data[i][0]} {data[i][1][0]}.{data[i][2][0]}.\n' +
                     f'качество = {data[i][3]}\nкоммуникативность = {data[i][4]}\nпрофессионализм = {data[i][5]}' +
                     f'\nнаходчивость = {data[i][6]}\nскорость = {data[i][7]}\nсреднее качество менеджера = {sr}\n\n')
        return temp
    return "Нет менеджеров для вывода статистики"


def refresh_reports(report, manager):
    with open('reports.txt', 'a') as f:
        f.write("\n" + manager + ": -" + report)


def get_user_info(token, table):
    if table == "Admins":
        cursor.execute('SELECT name, father_name FROM public."Admins" WHERE token=%s', (token, ))
    else:
        cursor.execute('SELECT name, father_name FROM public."Clients" WHERE token=%s', (token, ))
    temp = cursor.fetchall()
    return temp[0][0] + " " + temp[0][1]


def get_order_info(token, code):
    if code == 1:
        cursor.execute('SELECT time_to_delivery FROM public."Orders"' +
                       ' JOIN public."Clients" ON public."Orders".client_id = public."Clients".client_id' +
                       ' WHERE token = %s', (token,))
        temp = cursor.fetchall()
        if len(temp) > 0: date = temp[0][0].strftime("%d.%m.%Y, %H:%M")
        else: date = "---"
        if get_managers(token) == "К Вам не прикреплён ни один менеджер": managers = "---"
        else: managers = ", ".join(get_managers(token))
        return f'Список менеджеров по всем этапам заказа: {managers}\nСтатус заказа: Перевозка грузка\nСроки заказа: {date}'
    else:
        cursor.execute('SELECT token FROM public."Clients" WHERE last_name=%s', (list(token.split())[0],))
        return get_order_info(cursor.fetchall()[0][0], 1)


def get_clients():
    cursor.execute('SELECT last_name, name, father_name FROM public."Clients"')
    return [f"{i[0]} {i[1][0]}.{i[2][0]}." for i in cursor.fetchall()]
"""
