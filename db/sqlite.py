import pathlib
import sqlite3

from db.base import DatabaseMixin

SCRIPT_DIR = pathlib.Path(__file__).parent.absolute()


class SQLiteDatabase(DatabaseMixin):
    def __init__(self, *args,  **kwargs):
        self.connection = self.connect_to_database(
            kwargs.get("database_name"), kwargs.get("database_exist"))
        self.event_table_schema = """CREATE TABLE events
             (
                [id] INTEGER PRIMARY KEY,
                [url] text,
                [title] text,
                [date] text,
                [time] text,
                [venue] text,
                [street_address] text,
                [city] text,
                [state] text,
                [price] text
             )
        """
        self.create_tables(queries=[self.event_table_schema])

    def connect_to_database(self, database_name, database_exist):
        return sqlite3.connect(f"{SCRIPT_DIR}/{database_name}.db")

    def create_tables(self, queries):
        cursor = self.connection.cursor()
        for query in queries:
            cursor.execute(query)

        self.connection.commit()

    def insert(self, data):
        query = """
        INSERT INTO `events`
            (`url`, `title`, `date`, `time`, `venue`, `street_address`, 
            `city`, `state`, `price`)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        cursor = self.connection.cursor()
        cursor.executemany(query, data)
        self.connection.commit()
