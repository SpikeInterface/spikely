from spike_element import SpikeElement


class Postprocessor(SpikeElement):
    """Postprocessor class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.postprocessor_name)

    def run(self, input_payload):
        params_dict = {}
        params_dict['sorting'] = input_payload
        params = self._params
        for param in params:
            param_name = param['name']
            # param_type = param['type']
            # param_title = param['title']
            param_value = param['value']
            params_dict[param_name] = param_value
        sorting = self._interface_class(**params_dict)
        return sorting
