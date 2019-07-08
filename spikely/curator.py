from .spike_element import SpikeElement
import spikeextractors as se
from pathlib import Path
import spiketoolkit as st
import os


class Curator(SpikeElement):
    """Curator class"""

    def __init__(self, interface_class, interface_id):
        SpikeElement.__init__(self, interface_id, interface_class,
                              interface_class.curator_name)

    def run(self, input_payload, next_element):
        sorting_list = input_payload[0]
        output_folder_string = input_payload[1]
        recording = input_payload[2]
            
        curated_sorting_list = []
        for i, sorting in enumerate(sorting_list):
            params_dict = {}
            params_dict['sorting'] = sorting
            
            params = self._params
            for param in params:
                param_name = param['name']
                param_value = param['value']
                params_dict[param_name] = param_value
            curated_sorting = self._interface_class(**params_dict)
            curated_sorting_list.append(curated_sorting)
            if(next_element is None):
                output_folder_string_new = output_folder_string + '_phy_curated'
                output_folder = Path(output_folder_string_new).absolute()
                if(len(sorting_list) == 1):
                    curated_output_folder = output_folder
                else:
                    curated_output_folder = output_folder / str(i)
                if not curated_output_folder.is_dir():
                    os.makedirs(str(curated_output_folder))
                print("Saving curated results to " + str(curated_output_folder))
                st.postprocessing.export_to_phy(recording, curated_sorting, curated_output_folder)#, grouping_property='group')
                print("Done!")
        return curated_sorting_list, output_folder_string, recording
