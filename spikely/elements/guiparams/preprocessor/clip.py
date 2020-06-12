from spiketoolkit.preprocessing import clip

spif_init_func = clip

gui_params = [
    {
        "name": "a_min",
        "type": "float",
        "value": None,
        "default": None,
        "title": "Minimum value. If `None`, clipping is not performed on lower interval edge.",
    },
    {
        "name": "a_max",
        "type": "float",
        "value": None,
        "default": None,
        "title": "Maximum value. If `None`, clipping is not performed on upper interval edge.",
    },
]
