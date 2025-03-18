import sqlite3
import pandas as pd


def load_data(df: pd.DataFrame, db_name: str) -> None:
    """
    Загружает данные в БД
    Подразумевается, что БД уже создана и содержит таблицы для названий городов
    и данных о погоде
    А так же, что данные преобразованы должным образом

    Args:
        df (pd.DataFrame): преобразованные на предыдущем шаге данные
        db_name (str): имя БД
    """
    try:
        # Подключаемся к БД и создаем курсор для работы с ним
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Загружаем данные в БД
        # Первым делом загружаем данные о названиях городов в таблицу cities
        # Загрузка городов в cities с предотвращением дубликатов
        # Проверяем, если город уже есть в таблице cities, то пропускаем его
        cursor.executemany(
            "INSERT INTO cities (city, country) VALUES (?, ?) ON CONFLICT DO NOTHING",
            df[["city", "country"]].drop_duplicates().values.tolist(),
        )

        # Получение id городов
        city_ids = {}
        cursor.execute("SELECT city, id FROM cities")
        rows = cursor.fetchall()
        for row in rows:
            city_ids[row[0]] = row[1]

        # Подготовка данных для weather_data с использованием id городов
        weather_data = []
        for index, row in df.iterrows():
            city_id = city_ids.get(row["city"])
            if city_id is not None:
                weather_data.append(
                    (
                        city_id,
                        row["temperature"],
                        row["feels_like"],
                        row["humidity"],
                        row["weather"],
                        row["wind"],
                        row["date"],
                    )
                )

        # Загрузка данных в weather_data
        cursor.executemany(
            "INSERT INTO weather_data (city_id, temperature, feels_like, humidity, weather, wind, date) VALUES (?, ?, ?, ?, ?, ?, ?)",
            weather_data,
        )

        # Закрываем курсор
        cursor.close()

        # Подтверждаем изменения в БД и закрываем подключение
        conn.commit()
        conn.close()

    except Exception as e:
        # Обрабатываем ошибку, что бы не упал скрипт
        print(f"Ошибка при загрузке данных в БД: {e}")
        return

    print("Данные успешно загружены в БД")


# Пример использования:

# db_name = "weather_data.db"

# df = pd.DataFrame(
#     {
#         "name": ["Tokyo", "New York", "London"],
#         "country": ["JP", "US", "GB"],
#         "temp": [13.1, 13.1, 13.1],
#         "feels_like": [12.92, 12.92, 12.92],
#         "humidity": [94, 94, 94],
#         "weather": ["Mist", "Mist", "Mist"],
#         "wind": [0.51, 0.51, 0.51],
#         "dt": [1741777689, 1741777689, 1741777689],
#     }
# )

# load_data(df, db_name)

# Вывод:

# Данные успешно загружены в БД
