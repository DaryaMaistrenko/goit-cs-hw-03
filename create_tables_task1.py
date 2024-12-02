import psycopg2
from psycopg2 import Error
from contextlib import contextmanager
from colorama import init, Fore
from config import DB_CONFIG  # Ваш файл конфігурації

# Ініціалізація colorama
init(autoreset=True)

@contextmanager
def create_connection():
    """Створення з'єднання з PostgreSQL."""
    conn = None
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        yield conn
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback()
        print(f"{Fore.RED}Помилка підключення: {e}")
    finally:
        if conn:
            conn.close()


def create_table(conn, create_table_sql):
    """Створення таблиці на основі переданого SQL-запиту."""
    try:
        with conn.cursor() as cursor:
            cursor.execute(create_table_sql)
        print(f"{Fore.GREEN}Таблиця створена успішно.")
    except Error as e:
        print(f"{Fore.RED}Помилка створення таблиці: {e}")


if __name__ == "__main__":
    # SQL-запити для створення таблиць
    sql_create_users_table = """
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100) NOT NULL,
        email VARCHAR(100) UNIQUE NOT NULL
    );
    """
    sql_create_statuses_table = """
    CREATE TABLE IF NOT EXISTS statuses (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE NOT NULL
    );
    """
    sql_create_tasks_table = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100) NOT NULL,
        description TEXT,
        status_id INTEGER REFERENCES statuses(id) ON DELETE CASCADE,
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    );
    """

    # Словник для всіх таблиць
    table_creation_queries = {
        "users": sql_create_users_table,
        "statuses": sql_create_statuses_table,
        "tasks": sql_create_tasks_table,
    }

    # Підключення до бази даних і створення таблиць
    with create_connection() as conn:
        if conn:
            print(f"{Fore.BLUE}Підключення до бази даних успішне.")
            for table_name, query in table_creation_queries.items():
                print(f"{Fore.YELLOW}Створення таблиці '{table_name}'...")
                create_table(conn, query)
            print(f"{Fore.MAGENTA}Всі таблиці створені успішно!")
        else:
            print(f"{Fore.RED}Не вдалося створити з'єднання з базою даних.")
