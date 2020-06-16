import inspect
import os

import pkg_resources
from PyQt5 import QtGui, QtWidgets

from spikely.guiparams import get_gui_params, gui_params_file_exists
from . import spike_element as sp_spe
from spikely.elements.phy_exporter import PhyExporter


class SortingExporter(sp_spe.SpikeElement):
    @staticmethod
    def get_installed_spif_cls_list():
        """Returns sorted list of installed spif classes having gui_params files."""
        raw_list = [PhyExporter]

        # To be installed for Spikely purposes spif_class must have gui_params file
        cooked_list = [
            spif_class for spif_class in raw_list
            if gui_params_file_exists(
                SortingExporter.get_display_name_from_spif_class(spif_class),
                "exporter",
            )
        ]
        return sorted(cooked_list, key=lambda spif_class: spif_class.__name__)

    @staticmethod
    def get_display_name_from_spif_class(spif_class):
        return spif_class.__name__

    def __init__(self, spif_class):
        super().__init__(spif_class)

        if QtWidgets.QApplication.instance():
            self._display_icon = QtGui.QIcon(
                pkg_resources.resource_filename(
                    'spikely.resources', 'exporter.png'))
        else:
            self._display_icon = None

        self._param_list = get_gui_params(self.spif_class.__name__, "exporter")

    @property
    def display_name(self):
        return self.get_display_name_from_spif_class(self.spif_class)

    @property
    def display_icon(self):
        return self._display_icon

    def run(self, payload, next_elem):
        sorting_list = payload[0]
        recording = payload[2]

        for i, sorting in enumerate(sorting_list):
            params_dict = {}
            params_dict['sorting'] = sorting

            if 'recording' in inspect.signature(
                    self.spif_class.write_sorting).parameters:
                params_dict['recording'] = recording
            elif 'sampling_frequency' in inspect.signature(
                    (self.spif_class.write_sorting)).parameters:
                params_dict['sampling_frequency'] = \
                    recording.get_sampling_frequency()

            for param in self.param_list:
                param_name = param['name']
                param_value = param['value']

                if param_name == 'save_path':
                    if(len(sorting_list) == 1):
                        param_value = param_value
                    else:
                        path, file_name = os.path.split(param_value)
                        param_value = path + str(i) + '_' + file_name
                params_dict[param_name] = param_value

            print("Exporting to " + params_dict['save_path'])
            self.spif_class.write_sorting(**params_dict)
            print("Done exporting")