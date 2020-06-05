import configparser
import pathlib

import pkg_resources


def get_gui_params(display_name, element_pathname):
    """Construct a gui params structure from a config file

    Args:
        display_name: SpikeElement display_name mapped into .ini file name

    Returns:
        gui_param_list: List of gui_param dicts needed to populate the UI

    """

    gp_dirpath = pkg_resources.resource_filename(
        "spikely.elements", "guiparams/" + element_pathname
    )
    gp_filename = display_name.lower() + ".ini"

    gp_filepath = pathlib.Path(gp_dirpath) / gp_filename

    if not gp_filepath.is_file():
        raise FileExistsError(f"File not found: {gp_filename} in {gp_dirpath}")

    config = configparser.ConfigParser()
    config.read(gp_filepath)

    params_list = []
    for section in config.sections():
        # Name, type, and title are mandatory gui_params keys
        params = {
            "name": section,
            "type": config[section]["type"],
            "title": config[section]["title"],
        }

        # Value and default are either specified or unspecified together
        if config[section].get("value"):
            params["value"] = config[section]["value"]
            params["default"] = config[section]["default"]

        params_list.append(params)

    return params_list
