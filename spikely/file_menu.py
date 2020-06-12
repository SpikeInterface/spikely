"""Constructs File menu/actions, and executes user selected actions

During application initialization in spikely_main a menu bar is created as part
of the main window.  create_file_menu is called as part of that process to
populate the menu bar with a drop down menu of file related actions.

The core functionality within this module is support for saving and loading the
elements in the pipeline as JSON files. In collaboration with config.py, which
has methods to convert individual elements to/from serializable dictionary
objects, the _perform load/save methods in this module operate on the pipeline
as a whole.

"""

import json

from PyQt5 import QtWidgets

from spikely import PipelineModel, config

# Enables access to element list for both input and output
_pipeline_model = None


# Menu and Menu Action construction methods
def create_file_menu(main_window: QtWidgets.QMainWindow,
                     pipeline_model: PipelineModel) -> QtWidgets.QMenu:
    global _pipeline_model
    _pipeline_model = pipeline_model

    file_menu = QtWidgets.QMenu('&File', main_window)

    file_menu.addAction(_action(
        'Load Pipeline', 'Load pipeline from JSON file', _perform_load_action))
    file_menu.addAction(_action(
        'Save Pipeline', 'Save pipeline to JSON file', _perform_save_action))
    file_menu.addSeparator()
    file_menu.addAction(_action(
        'Share Output', 'Use terminal for all pipeline output',
        _toggle_share_state, checkable=True, checked=True))
    file_menu.addSeparator()
    file_menu.addAction(_action(
        'Exit', 'Terminate the application.',
        QtWidgets.QApplication.closeAllWindows))

    return file_menu


def _action(name, tip, slot, shortcut=None, checkable=False, checked=None):
    action = QtWidgets.QAction(name, config.get_main_window(),
                               checkable=checkable)
    action.setStatusTip(tip)
    action.triggered.connect(slot)
    if shortcut is not None:
        action.setShortcut(shortcut)
    if checkable and checked is not None:
        action.setChecked(checked)

    return action


# Menu Action execution methods

def _toggle_share_state(checked):
    _pipeline_model.share_output = checked


def _perform_load_action() -> None:
    """Loads current pipeline with elements from a previously saved JSON file

    Launches a file dialog box that allows the user to select a previously
    saved JSON file, attempts to decode it, and if successful adds the elements
    to the current pipeline replacing any elements extant in the pipeline.

    config.cvt_dict_to_elem() does most of the hard work, and throws exceptions
    if the element is no longer installed, or is no longer compatible with the
    version saved previously.

    """
    global _pipeline_model

    options = QtWidgets.QFileDialog.Options()
    options |= QtWidgets.QFileDialog.DontUseNativeDialog
    file_name, _filter = QtWidgets.QFileDialog.getOpenFileName(
            config.get_main_window(), caption='Open File',
            filter='JSON (*.json)', options=options)

    if file_name:
        _pipeline_model.clear()
        try:
            with open(file_name, 'r') as json_file:
                elem_dict_list = json.load(json_file)

            for elem_dict in elem_dict_list:
                elem = config.cvt_dict_to_elem(elem_dict)
                _pipeline_model.add_element(elem)

        except (json.decoder.JSONDecodeError, ValueError) as e:
            QtWidgets.QMessageBox.warning(
                config.get_main_window(), 'JSON File Load Failure',
                f'Failed to load {file_name}: {str(e)}')
            _pipeline_model.clear()

        except Exception as e:
            QtWidgets.QMessageBox.warning(
                config.get_main_window(), 'JSON File Load Failure',
                f'Unspecified exception: {str(e)}')
            _pipeline_model.clear()


def _perform_save_action() -> None:
    """Saves current pipeline of elements to a user specified JSON file

    Launches a file dialog box that allows the user to specifiy a JSON file,
    attempts to encode the element pipeline, and if successful writes out the
    decoded element pipelin in JSON format to file.

    config.cvt_elem_to_dict() does most of the hard work, by extracting class
    and parameter data from the element that allows the element to be JSON
    encoded and reinstantiated later when the filed is read back in by
    _perform_load_action().

    """
    global _pipeline_model

    # TODO: _element_list is supposed to be private - use data() instead?
    element_list = _pipeline_model._element_list

    if element_list:
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        file_name, _filter = QtWidgets.QFileDialog.getSaveFileName(
            config.get_main_window(), caption='Save File',
            filter='JSON (*.json)', options=options)

        if file_name:
            if not file_name.lower().endswith('.json'):
                file_name = file_name + '.json'
            elem_dict_list = [config.cvt_elem_to_dict(element)
                              for element in element_list]

            with open(file_name, 'w') as json_file:
                json.dump(elem_dict_list, json_file)
