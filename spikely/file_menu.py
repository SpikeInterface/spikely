# Application file Menu construction and execution

import json
import PyQt5.QtWidgets as qw
from . import config
from . import pipeline_model as sp_pim

# Enables access to element list for both input and output
_pipeline_model = None


# Menu and Menu Action construction methods
def create_file_menu(main_window: qw.QMainWindow,
                     pipeline_model: sp_pim.PipelineModel) -> qw.QMenu:
    global _pipeline_model

    _pipeline_model = pipeline_model

    file_menu = qw.QMenu('&File', main_window)
    file_menu.addAction(_create_load_action(main_window))
    file_menu.addAction(_create_save_action(main_window))
    file_menu.addAction(_create_exit_action(main_window))
    return file_menu


def _create_load_action(main_window: qw.QMainWindow) -> qw.QAction:
    load_action = qw.QAction('Load Pipeline', main_window)
    load_action.setShortcut('Ctrl+L')
    load_action.setStatusTip('Load pipeline from JSON file.')
    load_action.triggered.connect(_perform_load_action)
    return load_action


def _create_save_action(main_window: qw.QMainWindow) -> qw.QAction:
    save_action = qw.QAction('Save Pipeline', main_window)
    save_action.setShortcut('Ctrl+S')
    save_action.setStatusTip('Save pipeline to JSON file.')
    save_action.triggered.connect(_perform_save_action)
    return save_action


def _create_exit_action(main_window: qw.QMainWindow) -> qw.QAction:
    exit_action = qw.QAction('Exit', main_window)
    exit_action.setShortcut('Ctrl+Q')
    exit_action.setStatusTip('Terminate the application')
    exit_action.triggered.connect(qw.QApplication.closeAllWindows)
    return exit_action


# Menu Action execution methods

def _perform_load_action() -> None:
    global _pipeline_model

    options = qw.QFileDialog.Options()
    options |= qw.QFileDialog.DontUseNativeDialog
    file_name, _filter = qw.QFileDialog.getOpenFileName(
            config.find_main_window(), caption='Open File',
            filter='JSON (*.json)', options=options)

    if file_name:
        _pipeline_model.clear()
        try:
            with open(file_name, 'r') as json_file:
                elem_dict_list = json.load(json_file)

            for elem_dict in elem_dict_list:
                elem = config.cvt_dict_to_elem(elem_dict)

                if not elem.spif_class.installed:
                    raise ValueError(
                        f"Cannot create {elem_dict['spif_cls_name']} - "
                        f" not installed on users's system")

                # if _param_list_mismatch(
                #         element.param_list, elem_dict['param_list']):
                #     raise ValueError(
                #         f"Cannot create {elem_dict['spif_cls_name']} - "
                #         f" parameters are not compatible")

                _pipeline_model.add_element(elem)

        except json.decoder.JSONDecodeError as e:
            qw.QMessageBox.warning(
                config.find_main_window(), 'JSON File Load Failure',
                f'Failed to load {file_name}: {str(e)}')

        except ValueError as e:
            qw.QMessageBox.warning(
                config.find_main_window(), 'JSON File Load Failure',
                f'Failed to load {file_name}: {str(e)}')

        except Exception as e:
            qw.QMessageBox.warning(
                config.find_main_window(), 'JSON File Load Failure',
                f'Unspecified exception: {str(e)}')


def _perform_save_action() -> None:
    global _pipeline_model

    element_list = _pipeline_model._elements

    if element_list:
        options = qw.QFileDialog.Options()
        options |= qw.QFileDialog.DontUseNativeDialog
        file_name, _filter = qw.QFileDialog.getSaveFileName(
            config.find_main_window(), caption='Save File',
            filter='JSON (*.json)', options=options)

        if file_name:
            elem_dict_list = [config.cvt_dict_to_elem(element)
                              for element in element_list]

            with open(file_name, 'w') as json_file:
                json.dump(elem_dict_list, json_file)


# def _param_list_mismatch(new_param_list, old_param_list):
