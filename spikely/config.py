# Constants and helper functions used by other spikely modules
import importlib
import PyQt5.QtWidgets as qw
import sys
from .elements import spike_element as sp_spe
import json

# Duration in milliseconds of timeout for temporary status messages
STATUS_MSG_TIMEOUT = 3500

# Identifier to get elem object from pipeline model data()
ELEMENT_ROLE = 0x100

# Column IDs used by QTableView to display elem parameter data
PARAM_COL, TYPE_COL, VALUE_COL = 0, 1, 2


def find_main_window():
    # Avoids a global. Used to specify parent for qw.QMessageBox popups
    for widget in qw.QApplication.instance().topLevelWidgets():
        if isinstance(widget, qw.QMainWindow):
            return widget

    # It is a dark day if we end up here
    print('<<spikely fatal error: Failed to find QMainWindow.>>',
          file=sys.stderr)
    sys.exit()


def cvt_elem_to_dict(elem: sp_spe.SpikeElement) -> dict:
    elem_dict = {
        "element_cls_name": elem.__class__.__name__,
        "element_mod_name": elem.__module__,
        "spif_cls_name": elem.spif_class.__name__,
        "spif_mod_name": elem.spif_class.__module__,
        "param_list": elem.param_list}

    return elem_dict


def cvt_dict_to_elem(elem_dict: dict) -> sp_spe.SpikeElement:
    elem_mod = importlib.import_module(elem_dict['element_mod_name'])
    elem_cls = getattr(elem_mod, elem_dict['element_cls_name'])
    spif_mod = importlib.import_module(elem_dict['spif_mod_name'])
    spif_cls = getattr(spif_mod, elem_dict['spif_cls_name'])

    elem = elem_cls(spif_cls)
    elem.param_list = elem_dict['param_list']

    return elem


def async_run(elem_list_str):

    elem_jdict_list = json.loads(elem_list_str)
    elem_list = [cvt_dict_to_elem(elem_jdict)
                 for elem_jdict in elem_jdict_list]

    payload = None
    last_elem_index = len(elem_list) - 1
    for count, elem in enumerate(elem_list):
        next_elem = elem_list[count + 1] \
            if count < last_elem_index else None
        payload = elem.run(payload, next_elem)
