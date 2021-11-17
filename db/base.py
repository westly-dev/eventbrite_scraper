from abc import abstractmethod

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
