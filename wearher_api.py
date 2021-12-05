import requests

API_KEY = "0d2bfe527fb9c3b0b300f2dad57aaa5c"
icon_url_template = "https://openweathermap.org/img/wn/%s@4x.png"


def get_weather(city, token=API_KEY):
    try:
        r = requests.get(
            f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric&lang=ru"
        )
        data = r.json()
        main_data = {
            "city": city,
            "cur_weather": data["main"]["temp"],
            "feels": data["main"]["feels_like"],
            "wind_speed": data["wind"]["speed"],
            "description": data["weather"][0]["description"],
            "icon_url": icon_url_template % data["weather"][0]["icon"]
        } 
        return main_data
    except Exception as ex:
        print(f"[ОШИБКА] Не удалось получить погоду: {ex}")
        return None