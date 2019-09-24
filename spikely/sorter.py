from spike_element import SpikeElement
import spikesorters as ss

import PyQt5.QtGui as qg
import pkg_resources

import copy


class Sorter(SpikeElement):
    @staticmethod
    def get_installed_spif_classes():
        return ss.installed_sorter_list

    def __init__(self, spif_class):
        super().__init__(spif_class)

        self._display_name = spif_class.__name__
        self._display_icon = qg.QIcon(
            pkg_resources.resource_filename(
                'spikely.resources', 'sorter.png'))
        self._params = copy.deepcopy(spif_class.sorter_gui_params)

    def fits_between(self, upstream, downstream):
        return not upstream and not isinstance(downstream, Sorter)

    @property
    def display_name(self):
        return self._display_name

    @property
    def display_icon(self):
        return self._display_icon

    def run(self, payload, downstream):

        spif_params = {param['name']: param['value'] for param
                       in self._params if not param.get('base_param')}
        spif_params['recording'] = payload
        sorter = self._spif_class(**spif_params)

        sub_params = {param['name']: param['value'] for param
                      in self._params if param.get('base_param')}
        sorter.set_params(**sub_params)

        sorter.run()

        output_folder_string = sub_params.get('output_folder')
        if output_folder_string is None:
            output_folder_string = 'tmp_' + sorter.sorter_name

        return sorter.get_result_list(), output_folder_string, payload
