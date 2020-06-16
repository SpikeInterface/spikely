import pkg_resources
import spikesorters as ss
from PyQt5 import QtGui, QtWidgets

from spikely.guiparams import get_gui_params, gui_params_file_exists
from . import spike_element as sp_spe


class Sorter(sp_spe.SpikeElement):
    @staticmethod
    def get_installed_spif_cls_list():
        """Returns sorted list of installed spif classes having gui_params files."""
        raw_list = ss.installed_sorter_list

        # Filter out installed spif classes with no gui_params files
        cooked_list = [
            spif_class for spif_class in raw_list
            if gui_params_file_exists(
                Sorter.get_display_name_from_spif_class(spif_class), "sorter"
            )
        ]
        return sorted(cooked_list, key=lambda spif_class: spif_class.sorter_name)

    @staticmethod
    def get_display_name_from_spif_class(spif_class):
        return spif_class.sorter_name

    def __init__(self, spif_class):
        super().__init__(spif_class)

        self._display_name = self.get_display_name_from_spif_class(spif_class)

        if QtWidgets.QApplication.instance():
            self._display_icon = QtGui.QIcon(
                pkg_resources.resource_filename("spikely.resources", "sorter.png")
            )
        else:
            self._display_icon = None

        self._param_list = get_gui_params(self._display_name, "sorter")

    @property
    def display_name(self):
        return self._display_name

    @property
    def display_icon(self):
        return self._display_icon

    def run(self, payload, next_elem):

        base_param_list = {
            param["name"]: param["value"]
            for param in self._param_list
            if param.get("base_param") and bool(param.get("base_param"))
        }
        print(base_param_list)
        base_param_list["recording"] = payload
        sorter = self._spif_class(**base_param_list)

        sub_param_list = {
            param["name"]: param["value"]
            for param in self._param_list
            if not param.get("base_param")
        }
        print(sub_param_list)
        sorter.set_params(**sub_param_list)

        sorter.run()

        output_folder_string = sub_param_list.get("output_folder")
        if output_folder_string is None:
            output_folder_string = "tmp_" + sorter.sorter_name

        return sorter.get_result_list(), output_folder_string, payload
