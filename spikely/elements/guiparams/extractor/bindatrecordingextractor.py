gui_params = [
    {
        "name": "file_path",
        "type": "file",
        "title": "Path to file (.dat)"},
    {
        "name": "sampling_frequency",
        "type": "float",
        "title": "Sampling rate in HZ"},
    {
        "name": "numchan",
        "type": "int",
        "title": "Number of channels"},
    {
        "name": "dtype",
        "type": "np.dtype",
        "title": "The dtype of underlying data (int16, float32, etc.)",
    },
    {
        "name": "recording_channels",
        "type": "int_list",
        "value": None,
        "default": None,
        "title": "List of recording channels",
    },
    {
        "name": "time_axis",
        "type": "int",
        "value": 0,
        "default": 0,
        "title": "If 0 traces are transposed to ensure (nb_sample, nb_channel) in the file"
                 " If 1, the traces shape (nb_channel, nb_sample) is kept in the file.",
    },
    {
        "name": "offset",
        "type": "int",
        "value": 0,
        "default": 0,
        "title": "Offset in binary file",
    },
    {
        "name": "gain",
        "type": "float",
        "value": None,
        "default": None,
        "title": "gain of the recordings",
    },
    {
        "name": "is_filtered",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If true, assume recording is filtered.",
    },
]
