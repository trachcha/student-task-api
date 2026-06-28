import sqlite3

DATABASE_NAME = "tasks.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    return connection


def initialize_db():
    connection = get_connection()

    connection.execute("CREATE TABLE IF NOT EXISTS tasks ("
                       "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "title TEXT NOT NULL,"
                       "completed BOOLEAN NOT NULL DEFAULT 0);")

    connection.commit()
    connection.close()
