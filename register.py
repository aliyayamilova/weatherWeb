from logging import error
from pywebio.output import put_button, put_buttons, put_column, put_image, put_markdown, put_row, toast
from pywebio.input import PASSWORD
from pywebio.pin import pin, put_input
from pywebio.session import go_app
from cookie_io import get_current_user_id, init_js_cookie_io

from sql import register_user
from utils import centered_container, margin_button_container
from PIL.Image import open as open_image


# редирект в случае пойманных куки
def redirect():
    id = get_current_user_id()
    
    if id != None:
        go_app('home_page', new_window=False)


# обёртка - при ошибке регистрации возвращает сообщение об ошибке
def register():
    answer = register_user(pin.name, pin.city, pin.username, pin.password)

    if(type(answer) is str):
        toast(answer, duration=3, color='error')

# переход на страницу авторизации
def to_login():
    go_app('auth_page', new_window=False)


# основной код страницы регистрации
def register_page():
    im = open_image("utils\pogoda_reg.png")
    centered_container(put_column([put_image(im)]))
    
    init_js_cookie_io()
    redirect()
    put_column([
        put_input('name', label='Имя'),
        put_input('city', label='Город'),
        put_input('username', label='Логин'),
        put_input('password', label='Пароль', type=PASSWORD)
    ])
    centered_container(
        put_row([
            margin_button_container(put_button(label="Зарегистрироваться", onclick=register, color='warning')),
            margin_button_container(put_button(label="Назад", onclick=to_login, color='warning'))
        ])
    )