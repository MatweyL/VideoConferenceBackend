from abc import abstractmethod


class AbstractCRUD:

    @abstractmethod
    def create(self, entity):
        pass

    @abstractmethod
    def read(self, pk, *args, **kwargs):
        pass

    @abstractmethod
    def update(self, entity, entity_to_update, *args, **kwargs):
        pass

    @abstractmethod
    def delete(self, pk, *args, **kwargs):
        pass
