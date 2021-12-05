from PIL.Image import open as open_image
from pywebio.output import put_button, put_column, put_image, put_markdown, put_row, put_text, use_scope
from pywebio.pin import pin, put_input
from pywebio.session import go_app
from home import logout, put_additional_info

from utils import centered_container, font_second, margin_button_container, put_empty_row
from wearher_api import get_weather
    

@use_scope('weather', clear=True)
def get_weather_info():
    data = get_weather(pin.city)
    if(data == None):
        return put_text(f'Не получилось получить погоду по городу <{pin.city}>!')
    return centered_container(
        put_column([
            put_image(data['icon_url']),
            put_markdown(f"# {data['city']}, {data['cur_weather']} °C, {data['description']}"),
            font_second(put_additional_info(data['wind_speed'], data['feels']))
        ])
    )


def back():
    go_app('home_page', new_window=False)


def weather_search_page():
    im = open_image("utils\pogoda_gorod.png")

    put_row(
            [put_image(im), 
                None, centered_container(put_column([
                    put_button(label="На главную", onclick=back, color="warning"),
                    put_button(label="Выйти", onclick=logout, color="warning")
                ]))
            ], size='60% 100px 40%'
        )  
    
    put_empty_row()
    put_empty_row()

    put_row([
        put_input('city'),
        margin_button_container(put_button(label='Поиск', onclick=get_weather_info, color='warning'))
    ])
