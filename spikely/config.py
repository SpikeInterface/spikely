# Constants and helper functions used by other spikely modules
import importlib
import sys

from PyQt5 import QtWidgets

from spikely import SpikeElement

# Duration in milliseconds of timeout for temporary status messages
STATUS_MSG_TIMEOUT = 3500

# Identifier to get elem object from pipeline model data()
ELEMENT_ROLE = 0x100

# Column IDs used by QTableView to display elem parameter data
PARAM_COL, TYPE_COL, VALUE_COL = 0, 1, 2


def get_main_window() -> QtWidgets.QMainWindow:
    """Returns the app's main window for use as message box parent."""
    for widget in QtWidgets.QApplication.instance().topLevelWidgets():
        if isinstance(widget, QtWidgets.QMainWindow):
            return widget

    # It is a dark day if we end up here
    print("<<spikely fatal error: Failed to find QMainWindow.>>",
          file=sys.stderr)
    sys.exit()


def cvt_elem_to_dict(elem: SpikeElement) -> dict:
    """Converts element to dictionary to enable JSON encoding.

    Elements cannot be directly json encoded, so this function stores and
    element's class and module names along its instance data in a dictionary.
    The dictionary can be encoded, and when decoded a new instance of the
    element can be instantiated.

    json encoded elements are saved to files to allow pipeline saves and loads,
    and also used to transfer pipelines as strings between processes.

    """

    if not isinstance(elem, SpikeElement):
        raise TypeError("elem must be a SpikeElement object")

    elem_dict = {
        "element_cls_name": elem.__class__.__name__,
        "element_mod_name": elem.__module__,
        "spif_cls_name": elem.spif_class.__name__,
        "spif_mod_name": elem.spif_class.__module__,
        "param_list": elem.param_list,
    }

    return elem_dict


def cvt_dict_to_elem(elem_dict: dict) -> SpikeElement:
    """ Converts an element dictionary into an element.

    Used as part of the json encode/decode process, this method "reconstitutes"
    an element from a dictionary of element instance data that had been json
    encoded.

    """

    if not isinstance(elem_dict, dict):
        raise TypeError("elem_dict must be a dict object")

    elem_mod = importlib.import_module(elem_dict["element_mod_name"])
    elem_cls = getattr(elem_mod, elem_dict["element_cls_name"])
    spif_mod = importlib.import_module(elem_dict["spif_mod_name"])
    spif_cls = getattr(spif_mod, elem_dict["spif_cls_name"])

    if not spif_cls.installed:
        # Abort if spif_class is no longer installed on system
        raise ValueError(
            f"Cannot create {elem_dict['spif_cls_name']} - "
            f" not installed on users's system"
        )

    elem = elem_cls(spif_cls)

    elem_param_name_set = {param["name"] for param in elem.param_list}

    dict_param_name_set = {param["name"] for param in elem_dict["param_list"]}

    if not dict_param_name_set.issubset(elem_param_name_set):
        # Abort if the old param list is not a subset of new one
        raise ValueError(
            f"Cannot create {elem_dict['spif_cls_name']} - "
            f" saved version incompatible with current version"
        )

    elem.param_list = elem_dict["param_list"]

    return elem
