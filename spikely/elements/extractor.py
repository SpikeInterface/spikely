# Python
import numpy as np
import copy
# PyQt
import PyQt5.QtGui as qg
import pkg_resources
import PyQt5.QtWidgets as qw
# spikely
from . import spike_element as sp_spe
import spikeextractors as se


class Extractor(sp_spe.SpikeElement):
    @staticmethod
    def get_installed_spif_cls_list():
        return se.installed_recording_extractor_list

    @staticmethod
    def get_display_name_from_spif_class(spif_class):
        return spif_class.extractor_name

    def __init__(self, spif_class):
        super().__init__(spif_class)

        self._display_name = self.get_display_name_from_spif_class(spif_class)

        if qw.QApplication.instance():
            self._display_icon = qg.QIcon(
                pkg_resources.resource_filename(
                    'spikely.resources', 'extractor.png'))
        else:
            self._display_icon = None

        self._param_list = copy.deepcopy(spif_class.extractor_gui_params)

        probe_path_dict = {
            'name': 'probe_path', 'type': 'file',
            'value': None, 'default': None,
            'title': 'Path to probe file (.csv or .prb)'
        }
        self._param_list.append(probe_path_dict)

        self._param_list.append({
            'name': 'channel_map', 'type': 'int_list', 'value': None,
            'default': None, 'title': "List of channel ids for underlying \
            channels to be be mapped. If None, then uses default ordering."})

        self._param_list.append({
            'name': 'channel_groups', 'type': 'int_list', 'value': None,
            'default': None, 'title': "List of channel groups of the \
            underlying channels. If None, then no groups given."})

    @property
    def display_name(self):
        return self._display_name

    @property
    def display_icon(self):
        return self._display_icon

    def run(self, payload, next_elem):
        spif_params_dict = {}
        probe_file = None
        for param in self.param_list:
            if param['name'] == 'probe_path':
                probe_file = param['value']
            elif param['name'] == 'channel_map':
                channel_map = param['value']
            elif param['name'] == 'channel_groups':
                channel_groups = param['value']
            else:
                spif_params_dict[param['name']] = param['value']

        recording = self._spif_class(**spif_params_dict)

        if probe_file:
            recording = recording.load_probe_file(
                probe_file, channel_map, channel_groups)
        else:
            if channel_map:
                assert np.all([
                    chan in channel_map for chan in
                    recording.get_channel_ids()]), "all channel_ids in " \
                        "'channel_map' must be in recording channel ids"
                recording = se.SubRecordingExtractor(
                    recording, channel_ids=channel_map)
            if channel_groups:
                recording.set_channel_groups(
                    recording.get_channel_ids(), channel_groups)

        return recording
