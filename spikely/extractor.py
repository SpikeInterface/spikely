from .spike_element import SpikeElement
import spikeextractors as se


class Extractor(SpikeElement):
    """Extractor class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.extractor_name)

    def run(self, input_payload, next_element):
        params = self._params
        params_dict = {}
        for param in params:
            param_name = param['name']
            param_value = param['value']
            if(param_name == 'probe_path'):
                probe_path = param_value
            else:
                params_dict[param_name] = param_value
        recording = self._interface_class(**params_dict)
        if(not self._interface_class.has_default_locations):
            se.load_probe_file(recording, probe_path)
        return recording
