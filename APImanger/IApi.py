from abc import ABC, abstractmethod


class IApi(ABC):
    """
    Интерфейс для работы с API
    """

    __slots__ = ('urls', '__data')

    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def data(self):
        pass

    @abstractmethod
    def load_data(self):
        pass
