from .spike_element import SpikeElement
import spikeextractors as se


class Extractor(SpikeElement):
    """Extractor class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.extractor_name)

    def run(self, input_payload, next_element):
        if(not self._interface_class.has_default_locations):
            probe_path = self._params.pop(-1)['value']
        params = self._params
        params_dict = {}
        for param in params:
            param_name = param['name']
            # param_type = param['type']
            # param_title = param['title']
            param_value = param['value']
            params_dict[param_name] = param_value
        recording = self._interface_class(**params_dict)
        if(not self._interface_class.has_default_locations):
            se.load_probe_file(recording, probe_path)
        return recording
