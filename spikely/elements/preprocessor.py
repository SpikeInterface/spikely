# Python
import copy
import pkg_resources
# PyQt
import PyQt5.QtGui as qg
import PyQt5.QtWidgets as qw
# spikely
from . import spike_element as sp_spe
import spiketoolkit as st


class Preprocessor(sp_spe.SpikeElement):
    @staticmethod
    def get_installed_spif_cls_list():
        return st.preprocessing.preprocessinglist. \
            installed_preprocessers_list

    @staticmethod
    def get_display_name_from_spif_class(spif_class):
        return spif_class.preprocessor_name

    def __init__(self, spif_class):
        super().__init__(spif_class)

        self._display_name = self.get_display_name_from_spif_class(spif_class)

        if qw.QApplication.instance():
            self._display_icon = qg.QIcon(
                pkg_resources.resource_filename(
                    'spikely.resources', 'preprocessor.png'))
        else:
            self._display_icon = None

        self._param_list = copy.deepcopy(spif_class.preprocessor_gui_params)

    @property
    def display_name(self):
        return self._display_name

    @property
    def display_icon(self):
        return self._display_icon

    def run(self, payload, next_elem):
        spif_param_dict = {
            param['name']: param['value'] for param in self.param_list}
        spif_param_dict['recording'] = payload
        pp = self._spif_class(**spif_param_dict)
        return pp
