# Python
import pkg_resources
from inspect import getmembers, isfunction

# PyQt
from PyQt5 import QtGui
from PyQt5 import QtWidgets

# spikely
from . import spike_element as sp_spe
import spiketoolkit as st
from spikely.config import get_gui_params


class Preprocessor(sp_spe.SpikeElement):
    @staticmethod
    def get_installed_spif_cls_list():
        return st.preprocessing.preprocessinglist.installed_preprocessers_list

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

        # Function dictionary should only be created once, so move to class
        func_dict = {
            obj[0].replace("_", ""): obj[1]
            for obj in getmembers(st.preprocessing)
            if isfunction(obj[1])
        }
        self._preprocessor_func = func_dict[self._display_name.lower()]

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
