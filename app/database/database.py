import os
import sqlite3

DEFAULT_DATABASE_NAME = "tasks.db"


def get_database_name() -> str:
    return os.getenv("DATABASE_NAME", DEFAULT_DATABASE_NAME)


def get_connection() -> sqlite3.Connection:
    return sqlite3.connect(get_database_name())


def initialize_db() -> None:
    connection = get_connection()

    connection.execute("CREATE TABLE IF NOT EXISTS tasks ("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "title TEXT NOT NULL,"
                       "completed BOOLEAN NOT NULL DEFAULT 0);")

    connection.commit()
    connection.close()
