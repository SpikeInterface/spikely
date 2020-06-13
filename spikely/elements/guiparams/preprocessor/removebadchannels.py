from spiketoolkit.preprocessing import remove_bad_channels

spif_init_func = remove_bad_channels

gui_params = [
    {
        "name": "bad_channel_ids",
        "type": "int_list",
        "value": None,
        "default": None,
        "title": "List of bad channel ids (int)."
                 " If None, automatic removal will be done based on standard deviation.",
    },
    {
        "name": "bad_threshold",
        "type": "float",
        "value": 2,
        "default": 2,
        "title": "If automatic is used, the threshold for the standard deviation"
                 " over which channels are removed",
    },
    {
        "name": "seconds",
        "type": "float",
        "value": 10,
        "default": 10,
        "title": "If automatic is used, the number of seconds used to compute"
                 " standard deviations.",
    },
    {
        "name": "verbose",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If True output is verbose"},
]
