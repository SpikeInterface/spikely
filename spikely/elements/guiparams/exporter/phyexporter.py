from spiketoolkit.validation.quality_metric_classes.parameter_dictionaries import (
    get_validation_params,
)

class_default = get_validation_params()


gui_params = [
    {"name": "save_path", "type": "folder", "title": "Save path"},
    {
        "name": "compute_pc_features",
        "type": "bool",
        "value": True,
        "default": True,
        "title": "If True (default), pc features are computed.",
    },
    {
        "name": "compute_amplitudes",
        "type": "bool",
        "value": True,
        "default": True,
        "title": "If True (default), waveforms amplitudes are compute.",
    },
    {
        "name": "max_channels_per_template",
        "type": "int",
        "value": 3,
        "default": 3,
        "title": "Maximum channels per unit to return."
        " If None, all channels are returned.",
    },
    {
        "name": "n_comp",
        "type": "int",
        "value": class_default["n_comp"],
        "default": class_default["n_comp"],
        "title": "Number of PCA components (default 3).",
    },
    {
        "name": "max_spikes_for_pca",
        "type": "int",
        "value": class_default["max_spikes_for_pca"],
        "default": class_default["max_spikes_for_pca"],
        "title": "The maximum number of spikes to use to compute PCA.",
    },
    {
        "name": "grouping_property",
        "type": "str",
        "value": class_default["grouping_property"],
        "default": class_default["grouping_property"],
        "title": "Property to group channels. E.g. if the recording extractor has the"
        " 'group' property and 'grouping_property' is 'group', then waveforms"
        " are computed group-wise.",
    },
    {
        "name": "ms_before",
        "type": "float",
        "value": class_default["ms_before"],
        "default": class_default["ms_before"],
        "title": "Time period in ms to cut waveforms before the spike events.",
    },
    {
        "name": "ms_after",
        "type": "float",
        "value": class_default["ms_after"],
        "default": class_default["ms_after"],
        "title": "Time period in ms to cut waveforms after the spike events.",
    },
    {
        "name": "dtype",
        "type": "dtype",
        "value": class_default["dtype"],
        "default": class_default["dtype"],
        "title": "The dtype of underlying data (int16, float32, etc.)",
    },
    {
        "name": "max_spikes_per_unit",
        "type": "int",
        "value": class_default["max_spikes_per_unit"],
        "default": class_default["max_spikes_per_unit"],
        "title": "The maximum number of spikes to extract per unit.",
    },
    {
        "name": "compute_property_from_recording",
        "type": "bool",
        "value": class_default["compute_property_from_recording"],
        "default": class_default["compute_property_from_recording"],
        "title": "If True and 'grouping_property' is given, the property of each unit"
        " is assigned as the corresponding property of the recording extractor"
        " channel on which the average waveform is the largest",
    },
    {
        "name": "n_jobs",
        "type": "int",
        "value": class_default["n_jobs"],
        "default": class_default["n_jobs"],
        "title": "Number of parallel jobs (default 1).",
    },
    {
        "name": "method",
        "type": "str",
        "value": class_default["method"],
        "default": class_default["method"],
        "title": "If 'absolute' (default), amplitudes are absolute amplitudes"
        " in uV are returned. If 'relative', amplitudes are returned"
        " as ratios between waveform amplitudes and template amplitudes.",
    },
    {
        "name": "peak",
        "type": "str",
        "value": class_default["peak"],
        "default": class_default["peak"],
        "title": "If maximum channel has to be found among negative peaks ('neg'),"
        " positive ('pos') or both ('both' - default)",
    },
    {
        "name": "frames_before",
        "type": "int",
        "value": class_default["frames_before"],
        "default": class_default["frames_before"],
        "title": "Frames before peak to compute amplitude.",
    },
    {
        "name": "frames_after",
        "type": "int",
        "value": class_default["frames_after"],
        "default": class_default["frames_after"],
        "title": "Frames after peak to compute amplitude.",
    },
    {
        "name": "recompute_info",
        "type": "bool",
        "value": class_default["recompute_info"],
        "default": class_default["recompute_info"],
        "title": "If True, will always re-extract waveforms and templates.",
    },
    {
        "name": "save_property_or_features",
        "type": "bool",
        "value": class_default["save_property_or_features"],
        "default": class_default["save_property_or_features"],
        "title": "If True, will store all calculated features and properties.",
    },
    {
        "name": "verbose",
        "type": "bool",
        "value": class_default["verbose"],
        "default": class_default["verbose"],
        "title": "If True output is verbose.",
    },
    {
        "name": "memmap",
        "type": "dtype",
        "value": class_default["memmap"],
        "default": class_default["memmap"],
        "title": "If True, waveforms are saved as memmap object (recommended"
        " for long recordings with many channels.",
    },
    {
        "name": "joblib_backend",
        "type": "str",
        "value": class_default["joblib_backend"],
        "default": class_default["joblib_backend"],
        "title": "The backend for joblib (default is 'loky')",
    },
    {
        "name": "seed",
        "type": "int",
        "value": class_default["seed"],
        "default": class_default["seed"],
        "title": "Random seed for extracting waveforms and pcs.",
    },
]
