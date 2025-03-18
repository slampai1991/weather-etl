import os
import db_init
import pandas as pd
import src.extract as e
import src.transform as t
import src.load as l
from dotenv import load_dotenv

# Загружаем переменные из .env файла при помощи библиотеки dotenv
# https://pypi.org/project/python-dotenv/
# Это позволит нам скрыть ключи API в файле .env и не публиковать их в репозитории
load_dotenv()

if __name__ == "__main__":
    api_key = os.environ.get("api_key")  # Заполняем переменную из .env
    cities = [
        "Tokyo",
        "New York",
        "London",
        "Paris",
        "Sydney",
        "Amsterdam",
        "Oslo",
        "Buenos Aires",
        "Rio de Janeiro",
        "Cape Town",
        "Brisbane",
    ]  # Список городов

    # Инициализируем БД
    db_name = "weather_data.db"
    db_init.initialize_database(db_name)

    for city in cities:

        # Извлекаем данные о погоде
        weather_data = e.extract(api_key, city)

        # Преобразуем данные и загружаем в БД
        if weather_data:
            transformed_data = t.transform_data(weather_data)
            l.load_data(transformed_data, os.path.join("data", db_name))

        else:
            print("Ошибка при получении данных о погоде")

    print("Программа завершена")
