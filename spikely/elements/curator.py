
import inspect
import shutil
from pathlib import Path

from PyQt5 import QtGui
from PyQt5 import QtWidgets
import pkg_resources

from . import spike_element as sp_spe
import spikeextractors as se
import spiketoolkit as st
from spikely.guiparams import get_gui_params, get_spif_init_func, gui_params_file_exists


class Curator(sp_spe.SpikeElement):
    @staticmethod
    def get_installed_spif_cls_list():
        """Returns sorted list of installed spif classes having gui_params files."""
        raw_list = st.validation.curation_list.installed_curation_list

        # To be installed for Spikely purposes spif_class must also have gui_params file
        cooked_list = [
            spif_class for spif_class in raw_list
            if gui_params_file_exists(
                Curator.get_display_name_from_spif_class(spif_class), "curator"
            )
        ]

        return sorted(cooked_list, key=lambda spif_class: spif_class.curator_name)

    @staticmethod
    def get_display_name_from_spif_class(spif_class):

        display_name = spif_class.curator_name
        if not display_name.endswith("s"):
            display_name += "s"

        return display_name

    def __init__(self, spif_class):
        super().__init__(spif_class)

        self._display_name = self.get_display_name_from_spif_class(spif_class)

        if QtWidgets.QApplication.instance():
            self._display_icon = QtGui.QIcon(
                pkg_resources.resource_filename(
                    'spikely.resources', 'curator.png'))
        else:
            self._display_icon = None

        self._param_list = get_gui_params(self._display_name, "curator")
        self._curation_func = get_spif_init_func(self._display_name, "curator")

    @property
    def display_name(self):
        return self._display_name

    @property
    def display_icon(self):
        return self._display_icon

    def run(self, payload, next_element):

        sorting_list = payload[0]
        output_folder_str = payload[1]
        recording = payload[2]

        if not next_element:
            output_folder_str_new = output_folder_str + '_curated'
            output_folder = Path(output_folder_str_new).absolute()
            if output_folder.is_dir():
                shutil.rmtree(output_folder)
            output_folder.mkdir()

        curated_sorting_list = []
        for i, sorting in enumerate(sorting_list):
            params_dict = {}
            params_dict['sorting'] = sorting

            if 'recording' in \
                    inspect.signature(self._curation_func).parameters:
                params_dict['recording'] = recording
            elif 'sampling_frequency' in \
                    inspect.signature(self._curation_func).parameters:
                params_dict['sampling_frequency'] = \
                    recording.get_sampling_frequency()

            for param in self.param_list:
                param_name = param['name']
                param_value = param['value']
                params_dict[param_name] = param_value

            curated_sorting = self._curation_func(**params_dict)
            curated_sorting_list.append(curated_sorting)

            if not next_element:
                print("No Exporter chosen. Defaulting to "
                      "the .npz format.")
                if len(sorting_list) == 1:
                    file_name = 'curated_output.npz'
                else:
                    file_name = str(i) + '_curated_output.npz'

                se.NpzSortingExtractor.write_sorting(curated_sorting,
                    output_folder / file_name)  # noqa: E128
                print("Saved curated results to " + str(output_folder))

        return curated_sorting_list, output_folder_str, recording
