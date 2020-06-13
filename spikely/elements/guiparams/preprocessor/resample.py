from spiketoolkit.preprocessing import resample

spif_init_func = resample

gui_params = [
    {
        "name": "resample_rate",
        "type": "float",
        "title": "The resampling frequency."
    },
]
