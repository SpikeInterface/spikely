from . import spike_element as sp_spe
import spikesorters as ss

import PyQt5.QtGui as qg
import PyQt5.QtWidgets as qw
import pkg_resources

import copy


class Sorter(sp_spe.SpikeElement):
    @staticmethod
    def get_installed_spif_cls_list():
        return ss.installed_sorter_list

    @staticmethod
    def get_display_name_from_spif_class(spif_class):
        return spif_class.sorter_name

    def __init__(self, spif_class):
        super().__init__(spif_class)

        self._display_name = self.get_display_name_from_spif_class(spif_class)

        if qw.QApplication.instance():
            self._display_icon = qg.QIcon(
                pkg_resources.resource_filename(
                    'spikely.resources', 'exporter.png'))
        else:
            self._display_icon = None

        self._param_list = copy.deepcopy(spif_class.sorter_gui_params)

    @property
    def display_name(self):
        return self._display_name

    @property
    def display_icon(self):
        return self._display_icon

    def run(self, payload, next_elem):

        spif_param_list = {param['name']: param['value'] for param
                           in self._param_list if param.get('base_param')}
        spif_param_list['recording'] = payload
        sorter = self._spif_class(**spif_param_list)

        sub_param_list = {param['name']: param['value'] for param
                          in self._param_list if not param.get('base_param')}
        sorter.set_params(**sub_param_list)

        sorter.run()

        output_folder_string = sub_param_list.get('output_folder')
        if output_folder_string is None:
            output_folder_string = 'tmp_' + sorter.sorter_name

        return sorter.get_result_list(), output_folder_string, payload
