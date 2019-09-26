# Python
import copy
import pkg_resources
# PyQt
import PyQt5.QtGui as qg
# spikely
from . import spike_element as sp_spe
import spiketoolkit as st
from . import extractor as sp_ext
from . import sorter as sp_sor


class Preprocessor(sp_spe.SpikeElement):
    @staticmethod
    def get_installed_spif_classes():
        return st.preprocessing.preprocessinglist. \
            installed_preprocessers_list

    def __init__(self, spif_class):
        super().__init__(spif_class)

        self._display_name = spif_class.__name__
        self._display_icon = qg.QIcon(
            pkg_resources.resource_filename(
                'spikely.resources', 'preprocessor.png'))
        self._params = copy.deepcopy(spif_class.preprocessor_gui_params)

    def fits_between(self, above, below):
        ok_above = [None.__class__, sp_ext.Extractor, Preprocessor]
        ok_below = [None.__class__, sp_sor.Sorter, Preprocessor]
        return above.__class__ in ok_above and below.__class__ in ok_below

    @property
    def display_name(self):
        return self._display_name

    @property
    def display_icon(self):
        return self._display_icon

    def run(self, payload, downstream):
        spif_params = {param['name']: param['value'] for param in self._params}
        spif_params['recording'] = payload
        pp = self._spif_class(**spif_params)
        return pp
