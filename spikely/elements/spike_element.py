from abc import ABC, abstractmethod


class SpikeElement(ABC):

    # Abstract methods

    @staticmethod
    @abstractmethod
    def get_installed_spif_cls_list():
        pass

    @staticmethod
    @abstractmethod
    def get_display_name_from_spif_class(spif_class):
        pass

    @abstractmethod
    def run(self, payload, next_elem):
        pass

    @property
    @abstractmethod
    def display_name(self):
        pass

    @property
    @abstractmethod
    def display_icon(self):
        pass

    # Concrete base class methods

    def __init__(self, spif_class):
        self._spif_class = spif_class
        self._param_list = None

    @property
    def spif_class(self):
        return self._spif_class

    @property
    def param_list(self):
        return self._param_list

    @param_list.setter
    def param_list(self, param_list):
        self._param_list = param_list
