from spiketoolkit.preprocessing import notch_filter

spif_init_func = notch_filter

gui_params = [
    {
        "name": "freq",
        "type": "float",
        "value": 3000.0,
        "default": 3000.0,
        "title": "The target frequency of the notch filter.",
    },
    {
        "name": "q",
        "type": "int",
        "value": 30,
        "default": 30,
        "title": "The quality factor of the notch filter.",
    },
    {
        "name": "chunk_size",
        "type": "int",
        "value": 30_000,
        "default": 30_000,
        "title": "The chunk size to be used for the filtering.",
    },
    {
        "name": "cache_to_file",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If True, filtered traces are computed and cached all"
                 " at once on disk in temp file.",
    },
    {
        "name": "cache_chunks",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If True then each chunk is cached in memory (in a dict).",
    },
]
