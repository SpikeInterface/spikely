from spiketoolkit.preprocessing import normalize_by_quantile

spif_init_func = normalize_by_quantile

gui_params = [
    {
        "name": "scale",
        "type": "float",
        "value": 1.0,
        "default": 1.0,
        "title": "Scale for the output distribution"
    },
    {
        "name": "median",
        "type": "float",
        "value": 0.0,
        "default": 0.0,
        "title": "Median for the output distribution"},
    {
        "name": "q1",
        "type": "float",
        "value": 0.01,
        "default": 0.01,
        "title": "Lower quantile used for measuring the scale",
    },
    {
        "name": "q2",
        "type": "float",
        "value": 0.99,
        "default": 0.99,
        "title": "Upper quantile used for measuring the scale",
    },
    {
        "name": "seed",
        "type": "int",
        "value": 0,
        "default": 0,
        "title": "Random seed for reproducibility.",
    },
]
