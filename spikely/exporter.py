from spikely.spike_element import SpikeElement
import spikeextractors as se
from pathlib import Path
import spiketoolkit as st
import inspect
import os
import shutil
import copy


class Exporter(SpikeElement):
    """Exporter class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.exporter_name)
        self._params = copy.deepcopy(interface_class.exporter_gui_params)

    def run(self, input_payload, next_element):
        sorting_list = input_payload[0]
        recording = input_payload[2]
            
        if self.name == 'NwbSortingExporter':
            nwbfile_kwargs = {}
        for i, sorting in enumerate(sorting_list):
            params_dict = {}
            params_dict['sorting'] = sorting
            if 'recording' in inspect.getargspec(self._interface_class.write_sorting).args:
                params_dict['recording'] = recording
            elif 'sampling_frequency' in inspect.getargspec(self._interface_class.write_sorting).args:
                params_dict['sampling_frequency'] = recording.get_sampling_frequency()
            params = self._params
            for param in params:
                param_name = param['name']
                param_value = param['value']
                if param_name == 'save_path':
                    if(len(sorting_list) == 1):
                        param_value = param_value
                    else:
                        param_value = param_value + str(i)
                if param_name == 'identifier':
                    nwbfile_kwargs[param_name] = param_value
                if param_name == 'session_description':
                    nwbfile_kwargs[param_name] = param_value
                params_dict[param_name] = param_value
            if self.name == 'NwbSortingExporter':
                params_dict['nwbfile_kwargs'] = nwbfile_kwargs
            self._interface_class.write_sorting(**params_dict)
            print("Done Exporting!")
