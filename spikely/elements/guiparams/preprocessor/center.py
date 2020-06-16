from spiketoolkit.preprocessing import center

spif_init_func = center

gui_params = [
    {
        "name": "mode",
        "type": "str",
        "value": "median",
        "default": "median",
        "title": "median (default) or mean."
    },
    {
        "name": "seconds",
        "type": "float",
        "value": 10,
        "default": 10,
        "title": "Number of seconds used to compute center.",
    },
    {
        "name": "n_snippets",
        "type": "int",
        "value": 10,
        "default": 10,
        "title": "Number of snippets in which the total 'seconds' are divided spanning"
                 " the recording duration."
    },
]
