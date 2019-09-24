import PyQt5.QtWidgets as qw
import json
import importlib
import spikely.config as cfg

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
            parent=cfg.find_main_window(), caption='Open File',
            filter='JSON (*.json)', options=options)

    if file_name:
        _pipeline_model.clear()
        with open(file_name, 'r') as json_file:
            elem_dict_list = json.load(json_file)

        for elem_dict in elem_dict_list:
            elem_mod = importlib.import_module(elem_dict['element_mod_name'])
            elem_cls = getattr(elem_mod, elem_dict['element_cls_name'])
            spif_mod = importlib.import_module(elem_dict['spif_mod_name'])
            spif_cls = getattr(spif_mod, elem_dict['spif_cls_name'])

            element = elem_cls(spif_cls)
            element.params = elem_dict['params']

            _pipeline_model.add_element(element)


def _perform_save_action():
    global _pipeline_model

    elements = _pipeline_model._elements

    if elements:
        options = qw.QFileDialog.Options()
        options |= qw.QFileDialog.DontUseNativeDialog
        file_name, _filter = qw.QFileDialog.getSaveFileName(
            parent=cfg.find_main_window(), caption='Save File',
            filter='JSON (*.json)', options=options)

        if file_name:
            elem_dict_list = [
                _cvt_elem_to_dict(element) for element in elements]

            with open(file_name, 'w') as json_file:
                json.dump(elem_dict_list, json_file)


def _cvt_elem_to_dict(element):
    elem_dict = {
        "element_cls_name": element.__class__.__name__,
        "element_mod_name": element.__module__,
        "spif_cls_name": element.spif_class.__name__,
        "spif_mod_name": element.spif_class.__module__,
        "params": element.params
    }
    return elem_dict
