from spikely.spike_element import SpikeElement
import spikeextractors as se
from pathlib import Path
import spiketoolkit as st
import inspect
import os
import shutil
import copy


class Curator(SpikeElement):
    """Curator class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.curator_name)
        self._params = copy.deepcopy(interface_class.curator_gui_params)

    def run(self, input_payload, next_element):
        sorting_list = input_payload[0]
        output_folder_string = input_payload[1]
        recording = input_payload[2]
            
        curated_sorting_list = []
        for i, sorting in enumerate(sorting_list):
            params_dict = {}
            params_dict['sorting'] = sorting
            if 'recording' in inspect.getargspec(self._interface_class).args:
                params_dict['recording'] = recording
            elif 'sampling_frequency' in inspect.getargspec(self._interface_class).args:
                params_dict['sampling_frequency'] = recording.get_sampling_frequency()
            params = self._params
            for param in params:
                param_name = param['name']
                param_value = param['value']
                params_dict[param_name] = param_value
            curated_sorting = self._interface_class(**params_dict)
            curated_sorting_list.append(curated_sorting)
            
            if(next_element is None):
                print("No Exporter chosen. Defaulting to the .npz format.")
                output_folder_string_new = output_folder_string + '_curated'
                output_folder = Path(output_folder_string_new).absolute()
                if output_folder.is_dir():
                    shutil.rmtree(output_folder)
                output_folder.mkdir()
                if(len(sorting_list) == 1):
                    curated_output_folder = output_folder
                else:
                    curated_output_folder = output_folder / str(i)
                if curated_output_folder.is_dir():
                    shutil.rmtree(curated_output_folder)
                os.makedirs(str(curated_output_folder))
                se.NpzSortingExtractor.write_sorting(curated_sorting, curated_output_folder / 'curated_output.npz')
                print("Saved curated results to " + str(curated_output_folder))
        return curated_sorting_list, output_folder_string, recording
