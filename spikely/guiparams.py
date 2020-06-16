import importlib
from copy import deepcopy


def get_gui_params(filename, subpathname):
    """Load the gui_params list of param dictionaries for caller.

    Args:
        filename: gui_params filename maps to spif class display name
        subpathname: "curator", "exporter", "preprocessor", or "sorter"

    Returns:
        gui_param_list: List of gui_param dicts needed to populate the UI

    """
    module = get_gui_params_module(filename, subpathname)

    gui_params = None if not module else getattr(module, "gui_params", None)

    return deepcopy(gui_params)


def get_spif_init_func(filename, subpathname):
    """Load the gui_params list of param dictionaries for caller.

    Args:
        filename: gui_params filename maps to spif class display name
        subpathname: "curator", "exporter", "preprocessor", or "sorter"

    Returns:
       spif_init_func: Underlying spif function needed to instantiate spif class.

    """
    module = get_gui_params_module(filename, subpathname)

    spif_init_func = None if not module else getattr(module, "spif_init_func", None)

    return spif_init_func


def gui_params_file_exists(filename, subpathname):

    return get_gui_params_module(filename, subpathname) is not None


def get_gui_params_module(filename, subpathname):

    module_pathname = "." + subpathname + "." + filename.lower()

    try:
        module = importlib.import_module(module_pathname, "spikely.elements.guiparams")
    except ModuleNotFoundError:
        module = None

    return module
