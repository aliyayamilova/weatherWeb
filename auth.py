from pywebio.output import put_button, put_column, put_error, put_image, put_row
from pywebio.input import PASSWORD
from pywebio.pin import pin, put_input
from pywebio.session import go_app
from classes.user import User
from messages import show_message
from cookie_io import get_current_user_id, init_js_cookie_io, remove_all_cookies, set_cookie
from sql import validate_credentials
from utils import centered_container, margin_button_container
from PIL.Image import open as open_image

# переход на страницу регистрации
def register():
    go_app('register_page', new_window=False)


# вход в систем
def login():
    answer = validate_credentials(pin.username, pin.password)

    if(type(answer) is User):
        set_cookie('current_user_id', f'{answer.id}')
        go_app('home_page', new_window=False)
    else:
        put_error(answer, closable=True)


# редирект в случае пойманных куки
def redirect():
    id = get_current_user_id()
    
    if id != None:
        go_app('home_page', new_window=False)


# основной код страницы авторизации
def auth_page():
    init_js_cookie_io()
    redirect()
    remove_all_cookies()
    show_message()

    im = open_image("utils\pogoda_auth.png")
    centered_container(put_column([put_image(im)]))
    
    put_column([
        put_input('username', label='Логин'),
        put_input('password', label='Пароль', type=PASSWORD)
    ])
    centered_container(
        put_row([
            margin_button_container(put_button(label="Войти", onclick=login, color='warning')),
            margin_button_container(put_button(label="Регистрация", onclick=register, color='warning'))
        ])
    )
    