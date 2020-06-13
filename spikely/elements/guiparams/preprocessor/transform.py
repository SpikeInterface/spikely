from spiketoolkit.preprocessing import transform

spif_init_func = transform


gui_params = [
    {
        "name": "scalar",
        "type": "float",
        "value": 1.0,
        "default": 1.0,
        "title": "Scalar for the traces of the recording extractor.",
    },
    {
        "name": "offset",
        "type": "float",
        "value": 0.0,
        "default": 0.0,
        "title": "Offset for the traces of the recording extractor",
    },
]
