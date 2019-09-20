from abc import ABC, abstractmethod


class SpikeElement2(ABC):

    @staticmethod
    @abstractmethod
    def get_installed_spif_classes():
        pass

    def __init__(self, spif_class):
        self._spif_class = spif_class
        self._parameters = None

    @abstractmethod
    def fits_between(self, upstream, downstream):
        pass

    @abstractmethod
    def run(self, payload, downstream):
        pass

    @property
    def spif_class(self):
        return self._spif_class

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, p):
        self._parameters = p


class SpikeElement:
    """Base class for spifface elements"""

    def __init__(self, interface_id, interface_class, interface_name):
        self._interface_id = interface_id
        self._interface_class = interface_class
        self._name = interface_name

    @property
    def interface_id(self):
        return self._interface_id

    @property
    def interface_class(self):
        return self._interface_class

    @property
    def name(self):
        return self._name

    @property
    def params(self):
        return self._params

    @params.setter
    def params(self, params):
        self._params = params

    def setup(self):
        pass

    def run(self, input_payload, next_element):
        pass
