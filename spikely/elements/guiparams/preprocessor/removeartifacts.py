from spiketoolkit.preprocessing import remove_artifacts

spif_init_func = remove_artifacts

gui_params = [
    {
        "name": "triggers",
        "type": "int_list",
        "title": "List of ints with the stimulation trigger frames.",
    },
    {
        "name": "ms_before",
        "type": "float",
        "value": 0.5,
        "default": 0.5,
        "title": "Time interval in ms to remove before the trigger events.",
    },
    {
        "name": "ms_after",
        "type": "float",
        "value": 3.0,
        "default": 3.0,
        "title": "Time interval in ms to remove after the trigger events.",
    },
]
