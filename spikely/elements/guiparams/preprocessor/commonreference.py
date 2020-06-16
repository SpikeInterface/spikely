from spiketoolkit.preprocessing import common_reference

spif_init_func = common_reference

gui_params = [
    {
        "name": "reference",
        "type": "str",
        "value": "median",
        "default": "median",
        "title": "Reference type (median, average, or single).",
    },
    {
        "name": "groups",
        "type": "int_list_list",
        "value": None,
        "default": None,
        "title": "List of lists containins the channels for splitting the reference.",
    },
    {
        "name": "ref_channels",
        "type": "int_or_int_list",
        "value": None,
        "default": None,
        "title": "If no groups are specified, all channels are referenced to ref_channels.",
    },
    {
        "name": "dtype",
        "type": "str",
        "value": None,
        "default": None,
        "title": "dtype of the returned traces. If None, dtype is maintained.",
    },
    {
        "name": "verbose",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If True, output from SpikeInterface element is verbose when run.",
    },
]
