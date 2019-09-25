from spikely.spike_element import SpikeElement
import spiketoolkit as st
import spikely as sly

import PyQt5.QtGui as qg
import pkg_resources

import copy


class Preprocessor(SpikeElement):
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
        ok_above = [None.__class__, sly.Extractor, Preprocessor]
        ok_below = [None.__class__, sly.Sorter, Preprocessor]
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
