from spikesorters.kilosort import KilosortSorter
class_default = KilosortSorter._default_params

gui_params = [
    {
        "name": "output_folder",
        "type": "folder",
        "value": None,
        "default": None,
        "title": "Sorting output folder path.",
        "base_param": True,
    },
    {
        "name": "verbose",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If True, output from SpikeInterface element is verbose when run.",
        "base_param": True,
    },
    {
        "name": "grouping_property",
        "type": "str",
        "value": None,
        "default": None,
        "title": "Property name to be used for sorter output grouping.",
        "base_param": True,
    },
    {
        "name": "parallel",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If grouping property specifed, sort property groups in parallel if True.",
        "base_param": True,
    },
    {
        "name": "delete_output_folder",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "Delete specified or default output folder on completion if True.",
        "base_param": True,
    },
    # kilosort specific parameters
    {
        "name": "detect_threshold",
        "type": "float",
        "value": class_default["detect_threshold"],
        "default": class_default["detect_threshold"],
        "title": "Relative detection threshold",
    },
    {
        "name": "car",
        "type": "bool",
        "value": class_default["car"],
        "default": class_default["car"],
        "title": "car"
    },
    {
        "name": "useGPU",
        "type": "bool",
        "value": class_default["useGPU"],
        "default": class_default["useGPU"],
        "title": "If True, will use GPU",
    },
    {
        "name": "freq_min",
        "type": "float",
        "value": class_default["freq_min"],
        "default": class_default["freq_min"],
        "title": "Low-pass frequency",
    },
    {
        "name": "freq_max",
        "type": "float",
        "value": class_default["freq_max"],
        "default": class_default["freq_max"],
        "title": "High-pass frequency",
    },
    {
        "name": "ntbuff",
        "type": "int",
        "value": class_default["ntbuff"],
        "default": class_default["ntbuff"],
        "title": "Samples of symmetrical buffer " "for whitening and spike detection",
    },
    {
        "name": "Nfilt",
        "type": "int",
        "value": class_default["Nfilt"],
        "default": class_default["Nfilt"],
        "title": "Number of clusters to use "
        "(2-4 times more than Nchan, "
        "should be a multiple of 32)",
    },
    {
        "name": "NT",
        "type": "int",
        "value": class_default["NT"],
        "default": class_default["NT"],
        "title": "Batch size (try decreasing if "
        "out of memory) for GPU should be "
        "multiple of 32 + ntbuff	",
    },
]
