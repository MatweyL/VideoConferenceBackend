from abc import abstractmethod


class AbstractDB:

    @abstractmethod
    def save(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, *args, **kwargs):
        pass


class InMemoryDB(AbstractDB):

    def __init__(self):
        self._users = {}

    def save(self, *args, **kwargs):
        pass

    def get(self, *args, **kwargs):
        pass

    def update(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass
