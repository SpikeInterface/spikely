import copy


class SpikeElement:
    """Base class for SpikeInterface elements"""

    def __init__(self, interface_id, interface_class, interface_name):
        self._interface_id = interface_id
        self._interface_class = interface_class
        self._name = interface_name
        self._params = copy.deepcopy(interface_class.gui_params())

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

    def setup(self):
        pass

    def run(self, input_payload, next_element):
        pass
