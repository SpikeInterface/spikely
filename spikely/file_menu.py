import PyQt5.QtWidgets as qw
import json

from .extractor import Extractor
from .preprocessor import Preprocessor
from .sorter import Sorter
from .curator import Curator

import spikeextractors as se
import spiketoolkit as st
import spikesorters as ss

from . import config as cfg


_pipeline_model = None
_element_string = None


def create_file_menu(main_window, pipeline_model):
    global _pipeline_model
    _pipeline_model = pipeline_model
    file_menu = qw.QMenu('&File', main_window)
    file_menu.addAction(_create_load_action(main_window))
    file_menu.addAction(_create_save_action(main_window))
    file_menu.addAction(_create_exit_action(main_window))
    return file_menu


def _create_exit_action(main_window):
    exit_action = qw.QAction('Exit', main_window)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Terminate the application')
    exit_action.triggered.connect(qw.QApplication.closeAllWindows)
    return exit_action


def _create_load_action(main_window):
    load_action = qw.QAction('Load Pipeline', main_window)
    load_action.setShortcut('Ctrl+L')
    load_action.setStatusTip('Load contents of pipeline from file.')
    load_action.triggered.connect(_perform_load_action)
    return load_action


def _perform_load_action():
    global _element_string
    global _pipeline_model
    element_dict_list = json.loads(_element_string)

    for element_dict in element_dict_list:
        element_id = element_dict['element_id']
        element_class = _element_class_from_name(
            element_dict['class_name'], element_id)

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


def _create_save_action(main_window):
    save_action = qw.QAction('Save Pipeline', main_window)
    save_action.setShortcut('Ctrl+S')
    save_action.setStatusTip('Save contents of pipeline to file.')
    save_action.triggered.connect(_perform_save_action)
    return save_action


def _perform_save_action():
    global _pipeline_model
    global _element_string
    options = qw.QFileDialog.Options()
    options |= qw.QFileDialog.DontUseNativeDialog
    elements = _pipeline_model._elements

    if elements:
        file_name = qw.QFileDialog.getSaveFileName(
            parent=cfg.main_window, caption='Save Pileine as File',
            filter='JSON files (*.json)', options=options)

        element_dict_list = []
        for element in elements:
            element_dict_list.append(
                _cvt_element_to_dict(element))

        _element_string = json.dumps(
            element_dict_list)


def _cvt_element_to_dict(element):
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
    element_dict = element_dicts[element_id]
    return element_dict[class_name]
