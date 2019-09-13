from .spike_element import SpikeElement
import spikeextractors as se
import numpy as np


class Extractor(SpikeElement):
    """Extractor class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.extractor_name)
        if interface_class.has_default_locations:
            self._params.append({'name': 'probe_file', 'type': 'file', 'value':None, 'default':None, 'title': "Probe file name (.csv or .prb)"})
        else:
            self._params.append({'name': 'probe_file', 'type': 'file', 'title': "Path to probe file (.csv or .prb)"})
        self._params.append({'name': 'channel_map', 'type': 'int_list', 'value':None, 'default':None, 'title': "List of channel ids for the underlying to channels to be be mapped. If None, then uses default ordering."})
        self._params.append({'name': 'channel_groups', 'type': 'int_list', 'value':None, 'default':None, 'title': "List of channel groups of the underlying channels. If None, then no groups given."})


    def run(self, input_payload, next_element):
        params = self._params
        params_dict = {}
        probe_file = None
        for param in params:
            param_name = param['name']
            param_value = param['value']
            if(param_name == 'probe_file'):
                probe_file = param_value
            elif(param_name == 'channel_map'):
                channel_map = param_value
            elif(param_name == 'channel_groups'):
                channel_groups = param_value
            else:
                params_dict[param_name] = param_value
        recording = self._interface_class(**params_dict)
        if probe_file is not None:
            recording = recording.load_probe_file(probe_file, channel_map, channel_groups)
        else:
            if channel_map is not None:
                assert np.all([chan in channel_map for chan in recording.get_channel_ids()]), \
                "all channel_ids in 'channel_map' must be in the original recording channel ids"
                recording = se.SubRecordingExtractor(recording, channel_ids=channel_map)
            if channel_groups is not None:
                recording.set_channel_groups(recording.get_channel_ids(), channel_groups)

        return recording
