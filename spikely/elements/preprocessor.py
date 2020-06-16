# Python
import pkg_resources

# PyQt
from PyQt5 import QtGui
from PyQt5 import QtWidgets

# spikely
from . import spike_element as sp_spe
import spiketoolkit as st
from spikely.guiparams import get_gui_params, get_spif_init_func, gui_params_file_exists


class Preprocessor(sp_spe.SpikeElement):
    @staticmethod
    def get_installed_spif_cls_list():
        """Returns sorted list of installed spif classes having gui_params files."""
        raw_list = st.preprocessing.preprocessinglist.installed_preprocessers_list

        # To be installed for Spikely purposes spif_class must have gui_params file
        cooked_list = [
            spif_class
            for spif_class in raw_list
            if gui_params_file_exists(
                Preprocessor.get_display_name_from_spif_class(spif_class),
                "preprocessor",
            )
        ]

        return sorted(cooked_list, key=lambda spif_class: spif_class.preprocessor_name)

    @staticmethod
    def get_display_name_from_spif_class(spif_class):
        return spif_class.preprocessor_name

    def __init__(self, spif_class):
        super().__init__(spif_class)

        self._display_name = self.get_display_name_from_spif_class(spif_class)

        if QtWidgets.QApplication.instance():
            self._display_icon = QtGui.QIcon(
                pkg_resources.resource_filename("spikely.resources", "preprocessor.png")
            )
        else:
            self._display_icon = None

        self._param_list = get_gui_params(self._display_name, "preprocessor")
        self._preprocessor_func = get_spif_init_func(self._display_name, "preprocessor")

    @property
    def display_name(self):
        return self._display_name

    @property
    def display_icon(self):
        return self._display_icon

    def run(self, payload, next_elem):
        spif_param_dict = {param["name"]: param["value"] for param in self.param_list}
        spif_param_dict["recording"] = payload
        pp = self._preprocessor_func(**spif_param_dict)
        return pp
