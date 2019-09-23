from abc import ABC, abstractmethod


class SpikeElement(ABC):

    # Abstract methods

    @staticmethod
    @abstractmethod
    def get_installed_spif_classes():
        pass

    @abstractmethod
    def fits_between(self, upstream, downstream):
        pass

    @abstractmethod
    def run(self, payload, downstream):
        pass

    @property
    @abstractmethod
    def display_name(self):
        pass

    @property
    @abstractmethod
    def display_icon(self): pass

    # Concrete base class methods

    def __init__(self, spif_class):
        self._spif_class = spif_class
        self._params = None

    @property
    def spif_class(self):
        return self._spif_class

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, p):
        self._params = p
