import sqlite3
import os


def initialize_database(db_name: str) -> None:
    """
    Подключается к существующей БД Sqlite, либо создает БД если её нет.
    После подключения создает две таблицы: с названиями городов и данными о погоде.
    Таблицы будут связаны с помощью внешнего ключа.

    Args:
        db_name (str): имя БД
    """

    # Проверяем наличие директории БД в папке проекта
    # Создаем ее, если она отсутствует
    if not os.path.exists(r"data"):
        os.makedirs(r"data")
        print(r"Создана папка: data")

    try:
        # Создаем подключение к БД (если БД отсутствует, она будет создана)
        conn = sqlite3.connect(os.path.join(r"data", db_name))
        print("Подключение установлено")

    except Exception as e:
        print(f"Ошибка при создании БД: {e}")
        return

    # Сперва создаем курсор для работы с БД
    cursor = conn.cursor()
    # Создаем таблицы для хранения данных о погоде и названий городов
    # Свяжем их через внешний ключ

    # Таблица для хранения городов
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS cities (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT UNIQUE NOT NULL,
            country TEXT NOT NULL
            )
        """
    )

    # Таблица для хранения данных о погоде
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS weather_data (
            city_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            temperature REAL NOT NULL,
            feels_like REAL NOT NULL,
            weather TEXT NOT NULL,
            humidity REAL NOT NULL,
            wind REAL NOT NULL,
            FOREIGN KEY (city_id) REFERENCES cities (id)
            )
        """
    )

    print("Таблицы cities и weather_data созданы")

    # Сохраняем изменения в БД и закрываем подключение
    conn.commit()
    conn.close()
    print("Подключение закрыто")


# Пример использования:

# db_name = "weather_data.db"
# initialize_database(db_name)
#
# # После выполнения функции в папке проекта будет создан файл weather_data.db
