from spiketoolkit.preprocessing import bandpass_filter

spif_init_func = bandpass_filter

gui_params = [
    {
        "name": "freq_min",
        "type": "float",
        "value": 300.0,
        "default": 300.0,
        "title": "High-pass cutoff frequency.",
    },
    {
        "name": "freq_max",
        "type": "float",
        "value": 6_000,
        "default": 6_000,
        "title": "Low-pass cutoff frequency.",
    },
    {
        "name": "freq_wid",
        "type": "float",
        "value": 1_000,
        "default": 1_000,
        "title": "Width of the filter (when type is 'fft')",
    },
    {
        "name": "filter_type",
        "type": "str",
        "value": "fft",
        "default": "fft",
        "title": "fft or butter. The fft filter uses a kernel in the frequency domain."
                 " The butter filter uses scipy butter and filtfilt functions.",
    },
    {
        "name": "order",
        "type": "int",
        "value": 3,
        "default": 3,
        "title": "Order of the filter (if 'butter').",
    },
    {
        "name": "chunk_size",
        "type": "int",
        "value": 3_000,
        "default": 3_000,
        "title": "If True, filtered traces are computed and cached all at once"
                 " on disk in temp file.",
    },
    {
        "name": "cache_to_file",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If True, filtered traces are computed and cached all at once on"
                 " disk in temp file.",
    },
    {
        "name": "cache_chunks",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If True then each chunk is cached in memory (in a dict).",
    },
]
