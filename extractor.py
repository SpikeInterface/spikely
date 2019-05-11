from spike_element import SpikeElement


class Extractor(SpikeElement):
    """Extractor class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.extractor_name)

    def setup(self):
        params = self._params
        params_dict = {}
        for param in params:
            param_name = param['name']
            # param_type = param['type']
            # param_title = param['title']
            param_value = param['value']
            params_dict[param_name] = param_value
        self._recording = self._interface_class(**params_dict)

    def run(self, input_payload=None):
        params = self._params
        params_dict = {}
        for param in params:
            param_name = param['name']
            # param_type = param['type']
            # param_title = param['title']
            param_value = param['value']
            params_dict[param_name] = param_value
        recording = self._interface_class(**params_dict)
        return recording
