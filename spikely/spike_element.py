from abc import ABC, abstractmethod, abstractclassmethod


class SpikeElement2(ABC):

    @abstractclassmethod
    def spikeinter_hook_list(cls):
        pass

    def __init__(self, spikeinter_hook):
        self._spikeinter_hook = spikeinter_hook
        self._parameters = None

    @abstractmethod
    def fits_between(self, upstream, downstream):
        pass

    @abstractmethod
    def run(self, payload, downstream):
        pass

    @property
    def spikeinter_hook(self):
        return self._spikeinter_hook

    @property
    def parameters(self):
        return self._parameters

    @parameters.setter
    def parameters(self, p):
        self._parameters = p


class SpikeElement:
    """Base class for SpikeInterface elements"""

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
