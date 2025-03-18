import requests


def extract(api_key: str, city: str) -> dict | None:
    """
    Извлекаем данные о погоде в выбранном городе по API OpenWeatherMap

    Args:
        api_key (str): ключ для доступа к API
        city (str): название города, по которому получаем данные

    Returns:
        dict: необработанные данные о погоде
        None: если запрос не удался
    """

    # URL для получения данных о погоде заранее содержит параметр units
    # Который может принимать значения standard, metric, imperial
    # В зависимости от этого параметра возвращаются разные единицы измерения скорости ветра и температуры
    # Подбробнее https://openweathermap.org/weather-data
    # По умолчанию используется standard, но мы используем imperial
    # и получим температуру в Фаренгейтах и скорость в м/ч
    # что бы на этапе преобразования было что менять
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=imperial"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


# # Пример использования:

# api_key = "your_api_key"
# city = "Tokyo"

# weather_data = extract(api_key, city)

# if weather_data:
#     print(weather_data)

# # Output:

# {
#     "coord": {"lon": 139.6917, "lat": 35.6895},
#     "weather": [
#         {"id": 801, "main": "Clouds", "description": "few clouds", "icon": "02n"}
#     ],
#     "base": "stations",
#     "main": {
#         "temp": 48.58,
#         "feels_like": 40.62,
#         "temp_min": 45.79,
#         "temp_max": 49.66,
#         "pressure": 1008,
#         "humidity": 38,
#         "sea_level": 1008,
#         "grnd_level": 1006,
#     },
#     "visibility": 10000,
#     "wind": {"speed": 26.46, "deg": 340},
#     "clouds": {"all": 20},
#     "dt": 1742207439,
#     "sys": {
#         "type": 2,
#         "id": 268395,
#         "country": "JP",
#         "sunrise": 1742158183,
#         "sunset": 1742201382,
#     },
#     "timezone": 32400,
#     "id": 1850144,
#     "name": "Tokyo",
#     "cod": 200,
# }
