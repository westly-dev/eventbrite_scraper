from db.base import DatabaseMixin
from os import getenv

from mysql.connector import connect, Error, ProgrammingError

class MySQLDatabase(DatabaseMixin):
    def __init__(self, *args,  **kwargs):
        self.connection = self.connect_to_database(
            kwargs.get("database_name"), kwargs.get("database_exist"))
        self.event_table_schema = """
        CREATE TABLE `events` (
            `id` int(11) NOT NULL AUTO_INCREMENT,
            `url` TEXT,
            `title` TEXT,
            `date` TEXT,
            `time` TEXT,
            `venue` TEXT,
            `street_address` TEXT,
            `city` TEXT,
            `state` TEXT,
            `zipcode` INT(11),
            `map_url` TEXT,
            `price` TEXT,
            PRIMARY KEY (`id`)
        )"""
        self.create_tables(queries=[self.event_table_schema])

    def connect_to_database(self, database_name, database_exist=True):
        """
        Connect to database, creating the database if it does't exist.

        :param database_name: str representing database name
        :param database_exist: bool representing if exists
        :return: connection: connection to mysql db
        """
        try:
            if database_exist:
                return connect(
                    host="localhost",
                    user=getenv("DATABASE_USER"),
                    password=getenv("DATABASE_PASSWORD"),
                    database=database_name,
                )

            connection = connect(
                host="localhost",
                user=getenv("DATABASE_USER"),
                password=getenv("DATABASE_PASSWORD"),
            )
            create_db_query = f"CREATE DATABASE {database_name}"
            cursor = connection.cursor()
            cursor.execute(create_db_query)
            return connection

        except Error as e:
            print(e)

    def create_tables(self, queries):
        """
        :param connection:
        :param queries:
        :return:
        """
        with self.connection.cursor() as cursor:
            for query in queries:
                try:
                    cursor.execute(query)

                except ProgrammingError as e:
                    if e.errno == 1050:
                        print("Table exists, continuing")
                        continue
                    else:
                        print(query)
                        raise ProgrammingError

            self.connection.commit()

    def insert(self, data):
        query = """
        INSERT INTO `events`
            (`url`, `title`, `date`, `time`, `venue`, `street_address`,
            `city`, `state`, `zipcode`, `map_url`, `price`)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""

        with self.connection.cursor() as cursor:
            cursor.executemany(query, data)
            self.connection.commit()
