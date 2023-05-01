from abc import abstractmethod


class AbstractCRUD:

    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def read(self, pk, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, entity, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, pk, *args, **kwargs):
        pass
