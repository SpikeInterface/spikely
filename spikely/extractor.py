from spike_element import SpikeElement
import spikeextractors as se


class Extractor(SpikeElement):
    """Extractor class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.extractor_name)

    def run(self, input_payload, next_element):
        probe_path = self._params[-1]['value']
        params = self._params
        params_dict = {}
        for param in params[:-1]:
            param_name = param['name']
            # param_type = param['type']
            # param_title = param['title']
            param_value = param['value']
            params_dict[param_name] = param_value
        recording = self._interface_class(**params_dict)
        if(probe_path is not None):
            se.load_probe_file(recording, probe_path)
        return recording
