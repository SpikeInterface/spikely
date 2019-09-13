import PyQt5.QtWidgets as qw
import json

from spikely.extractor import Extractor
from spikely.preprocessor import Preprocessor
from spikely.sorter import Sorter
from spikely.curator import Curator
from spikely.spike_element import SpikeElement

import spikeextractors as se
import spiketoolkit as st
import spikesorters as ss

from spikely import config as cfg


# Provides access to pipeline elements
_pipeline_model = None


# Menu and Menu Action construction methods

def create_file_menu(main_window, pipeline_model):
    global _pipeline_model

    _pipeline_model = pipeline_model

    file_menu = qw.QMenu('&File', main_window)
    file_menu.addAction(_create_load_action(main_window))
    file_menu.addAction(_create_save_action(main_window))
    file_menu.addAction(_create_exit_action(main_window))
    return file_menu


def _create_load_action(main_window):
    load_action = qw.QAction('Load Pipeline', main_window)
    load_action.setShortcut('Ctrl+L')
    load_action.setStatusTip('Load pipeline from JSON file.')
    load_action.triggered.connect(_perform_load_action)
    return load_action


def _create_save_action(main_window):
    save_action = qw.QAction('Save Pipeline', main_window)
    save_action.setShortcut('Ctrl+S')
    save_action.setStatusTip('Save pipeline to JSON file.')
    save_action.triggered.connect(_perform_save_action)
    return save_action


def _create_exit_action(main_window):
    exit_action = qw.QAction('Exit', main_window)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Terminate the application')
    exit_action.triggered.connect(qw.QApplication.closeAllWindows)
    return exit_action


# Menu Action execution methods

def _perform_load_action():
    global _pipeline_model

    options = qw.QFileDialog.Options()
    options |= qw.QFileDialog.DontUseNativeDialog
    file_name, _filter = qw.QFileDialog.getOpenFileName(
            parent=cfg.main_window, caption='Open File',
            filter='JSON (*.json)', options=options)

    if file_name:
        _pipeline_model.clear()
        with open(file_name, 'r') as json_file:
            element_dict_list = json.load(json_file)

        for element_dict in element_dict_list:
            element_id = element_dict['element_id']
            element_class = _element_class_from_name(
                element_dict['class_name'], element_id)
            assert element_class.installed, \
                element_dict['class_name'] + " not installed."

            if element_id == cfg.EXTRACTOR:
                spike_element = Extractor(element_class, cfg.EXTRACTOR)
            elif element_id == cfg.PRE_PROCESSOR:
                spike_element = Preprocessor(element_class, cfg.PRE_PROCESSOR)
            elif element_id == cfg.SORTER:
                spike_element = Sorter(element_class, cfg.SORTER)
            elif element_id == cfg.CURATOR:
                spike_element = Curator(element_class, cfg.CURATOR)

            spike_element.params = element_dict['params']
            _pipeline_model.add_element(spike_element)


def _perform_save_action():
    global _pipeline_model

    elements = _pipeline_model._elements

    if elements:
        options = qw.QFileDialog.Options()
        options |= qw.QFileDialog.DontUseNativeDialog
        file_name, _filter = qw.QFileDialog.getSaveFileName(
            parent=cfg.main_window, caption='Save File',
            filter='JSON (*.json)', options=options)

        if file_name:
            element_dict_list = [
                _cvt_element_to_dict(element) for element in elements]

            with open(file_name, 'w') as json_file:
                json.dump(element_dict_list, json_file)


def _cvt_element_to_dict(element: SpikeElement):
    element_dict = {
        "class_name": element.name,
        "element_id": element.interface_id,
        "params": element.params
    }
    return element_dict


def _element_class_from_name(class_name, element_id):
    element_dicts = {
        cfg.EXTRACTOR: se.extractorlist.recording_extractor_dict,
        cfg.PRE_PROCESSOR: st.preprocessing.preprocesser_dict,
        cfg.SORTER: ss.sorter_dict,
        cfg.CURATOR: st.curation.curation_dict
    }
    return element_dicts[element_id][class_name]
