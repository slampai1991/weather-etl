import pandas as pd


def transform_data(raw_data: dict) -> pd.DataFrame:
    """
    Преобразует необработанные данные в очищенный и структурированный формат.

    Параметры:
        raw_data (dict): Необработанные данные

    Возвращает:
        pd.DataFrame: Преобразованные данные
    """
    try:
        # Извлекаем нужные данные из словаря и преобразуем при необходимости
        data = {
            "city": raw_data["name"],
            "country": raw_data["sys"]["country"],
            "temperature": round(
                (raw_data["main"]["temp"] - 32) * 5 / 9, 2
            ),  # преобразуем из Фаренгейта в Цельсии
            "feels_like": round(
                (raw_data["main"]["feels_like"] - 32) * 5 / 9, 2
            ),  # преобразуем из Фаренгейта в Цельсии
            "weather": raw_data["weather"][0]["main"],
            "humidity": raw_data["main"]["humidity"],
            "wind": round(
                raw_data["wind"]["speed"] * 0.44704, 2
            ),  # преобразуем из миль/ч в метры/с
            "date": pd.to_datetime(raw_data["dt"], unit="s").strftime(
                "%Y-%m-%d-%H:%M-%S"
            ),  # преобразуем дату в нужный формат
        }

        transformed_data = pd.DataFrame(
            data, index=[1]
        )  # Создаем DataFrame и индексируем с 1

    except Exception as e:
        raise Exception(f"Не удалось преобразовать данные в pd.DataFrame: {e}")

    return transformed_data


# Пример использования:

# raw_data = {
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

# result = transform_data(raw_data)

# print(result)


# # Output:

#     city country  temperature  feels_like weather  humidity   wind                date
# 1  Tokyo      JP         9.21        4.79  Clouds        38  11.83 2025-03-17 10:30:39
