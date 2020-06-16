from spiketoolkit.preprocessing import blank_saturation

spif_init_func = blank_saturation

gui_params = [
    {
        "name": "threshold",
        "type": "float",
        "value": None,
        "default": None,
        "title": "Threshold value (in absolute units) for saturation artifacts. "
                 "If None, the threshold will be determined from the 0.1 signal percentile.",
    },
    {
        "name": "seed",
        "type": "int",
        "value": 0,
        "default": 0,
        "title": "Random seed for reproducibility.",
    },
]
