from abc import ABC, abstractmethod


class DatabaseInterface(ABC):
    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def execute(self, query: str, params: tuple = ()):
        pass

    @abstractmethod
    def fetch_one(self, query, params: tuple = ()):
        pass

    @abstractmethod
    def fetch_all(self, query, params: tuple = ()):
        pass

    @abstractmethod
    def commit(self):
        pass

    @abstractmethod
    def rollback(self):
        pass
