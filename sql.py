import sqlite3
from typing import Any
from pywebio.session import go_app
from classes.user import User
from sqlite3 import Error
from messages import set_message


db = sqlite3.connect('db_weather.sqlite', check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)


# клиент бд
sql = db.cursor()


# запросы к бд
get_user_by_username_query = "select * from user where username = '%s'"
get_user_by_id_query = "select * from user where id = %s"
register_user_query = "insert into user (name, username, user_city, password) values ('%s', '%s', '%s', '%s')"


# логгер sql
def log(message):
    print(f'[SQL] {message}...')


# обёртка для функций sql - проверка на ошибки внутри sql
def sql_error_check(query_function) -> Any:
    def wrapper(*args, **kwargs):
        try:
            return query_function(*args, **kwargs)
        except Error as e:
            if(db): db.rollback()
            return f"Ошибка БД! {' '.join(e.args)}"
        except Exception as e:
            if(db): db.rollback()
            return f"Ошибка! {' '.join(e.args)}"
    return wrapper


# проверка пользователя
@sql_error_check
def validate_credentials(username: str, password: str) -> Any:
    sql.execute(get_user_by_username_query % username)
    user_tuple: tuple = sql.fetchone()
    if(user_tuple is None):
        return 'Пользователь не зарегистрован. Перейдите на страницу регистрации'
    else:
        user = User(user_tuple)
        if(user.password == password):
            return user
        else:
            return 'Логин и пароль не совпадают!'


# получение пользователя по id
def get_user_by_id(id: int):
    sql.execute(get_user_by_id_query % id)
    user_tuple: tuple = sql.fetchone()
    if(user_tuple is None):
        return None
    else:
        user = User(user_tuple)
        return user


# регистрация пользователя
@sql_error_check
def register_user(name: str, city: str, username: str, password: str) -> Any:
    sql.execute(get_user_by_username_query % username)
    user_tuple: tuple = sql.fetchone()
    if(user_tuple is not None):
        return 'Пользователь уже зарегистрирован. Выберете другой логин!'
    
    sql.execute(register_user_query % (name, username, city, password))
    db.commit()
    set_message('Вы успешно зарегистрировались!')
    go_app('auth_page', new_window=False)