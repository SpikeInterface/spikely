from .spike_element import SpikeElement


class Preprocessor(SpikeElement):
    """Preprocessor class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.preprocessor_name)

    def run(self, input_payload, next_element):
        params_dict = {}
        params_dict['recording'] = input_payload
        params = self._params
        for param in params:
            param_name = param['name']
            # param_type = param['type']
            # param_title = param['title']
            param_value = param['value']
            params_dict[param_name] = param_value
        pp = self._interface_class(**params_dict)
        return pp
