from spiketoolkit.preprocessing import whiten

spif_init_func = whiten


gui_params = [
    {
        "name": "chunk_size",
        "type": "int",
        "value": 30_000,
        "default": 30_000,
        "title": "The chunk size to be used for the filtering.",
    },
    {
        "name": "cache_chunks",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "IIf True, filtered traces are computed and"
                 " cached all at once (default False).",
    },
    {
        "name": "seed",
        "type": "int",
        "value": 0,
        "default": 0,
        "title": "Random seed for reproducibility.",
    },
]
