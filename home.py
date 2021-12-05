from pywebio.output import put_button, put_buttons, put_column, put_image, put_markdown, put_row, style
from pywebio.session import go_app
from cookie_io import get_current_user_id, init_js_cookie_io, remove_user_info
from sql import get_user_by_id
from utils import centered_container, font_second, put_empty_row
from styles import *
from wearher_api import get_weather
from PIL.Image import open as open_image

# глобальные переменные страницы
page_globals = {
    'current_user': None
}


cell_container_style = '''
    align-items: center;
    align-self: center;
    display: flex;
    flex-direction: column;
    margin: 20px;
    background-color: #efefef;
    border-radius: 10px;
    padding: 10px;
    width: 800px;
'''


# стереть глобальные переменные страницы
def clear_page_globals():
    global page_globals
    page_globals = {
        'current_user': None
    }


# получение пользователя из id в куки
def set_user_from_cookie():
    global page_globals
    id = get_current_user_id()
    if(id != None):
        user = get_user_by_id(id)
        if(user != None):
            page_globals['current_user'] = user


# выход из учетной записи
def logout():
    remove_user_info()
    clear_page_globals()
    go_app('auth_page', new_window=False)


# поиск по городу
def search():
    go_app('weather_search_page', new_window=False)


def put_additional_info(wind_speed, feels):
    return put_column([
        put_markdown(f"🌬️ Ветер: {wind_speed} м/с"),
        put_markdown(f"👋 Ощущается как: {feels} °C")
    ])


def current_weather():
    data = get_weather(page_globals['current_user'].user_city)
    return put_column([
        put_image(data['icon_url']),
        put_markdown(f"# {data['city']}, {data['cur_weather']} °C, {data['description']}"),
        font_second(put_additional_info(data['wind_speed'], data['feels']))
    ])


# домашнаяя страница
def home_page():
    init_js_cookie_io()
    set_user_from_cookie()

    im = open_image("https://i.ibb.co/ctJqGN5/pogoda.png")

    if(page_globals['current_user'] == None):
        go_app('auth_page', new_window=False)

    put_row(
            [put_image(im), 
                None, centered_container(put_column([
                    put_button(label="Ввести город", onclick=search, color="warning"),
                    put_button(label="Выйти", onclick=logout, color="warning")
                ]))
            ], size='60% 100px 40%'
        )  

    put_empty_row()

    centered_container(current_weather())

    
    

    
