
from abc import abstractmethod
from enum import Enum

from db.sqlite import SQLiteDatabase
from db.mysql import MySQLDatabase



class DatabaseMixin:
    @abstractmethod
    def connect_to_database(self, database_name, database_exist):
        raise NotImplementedError

    @abstractmethod
    def create_tables(self, queries):
        raise NotImplementedError

    @abstractmethod
    def insert(self, data):
        raise NotImplementedError

class DatabaseType(Enum):
    """
    Enum representing a database type.
    """

    SQLITE = ("sqlite", SQLiteDatabase)
    MYSQL = ("mysql", MySQLDatabase)

    @staticmethod
    def list():
        """
        :return: dir of string representations of database type
        """
        return dict(map(lambda output: (output.value[0], output.value[1]), DatabaseType))


class DatabaseFactory:
    supported_types = DatabaseType.list()

    @staticmethod
    def create_database(*args, **kwargs):
        if kwargs.get("database") not in DatabaseFactory.supported_types.keys():
            raise NotImplemented(
                f'Database type {kwargs.get("database")} is not yet supported.')

        cls_obj = DatabaseFactory.supported_types[kwargs.get("database")]
        obj = cls_obj(*args, **kwargs)
        return obj
