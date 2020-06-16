from spiketoolkit.validation.quality_metric_classes.parameter_dictionaries import (
    get_validation_params,
)
from spiketoolkit.curation import threshold_amplitude_cutoffs 
class_default = get_validation_params()
spif_init_func = threshold_amplitude_cutoffs

gui_params = [
    {
        "name": "threshold",
        "type": "float",
        "title": "The threshold for the given metric.",
    },
    {
        "name": "threshold_sign",
        "type": "str",
        "title": "If 'less', will threshold any metric less than the given threshold. \
                  If 'less_or_equal', will threshold any metric less than or equal to the given threshold. \
                  If 'greater', will threshold any metric greater than the given threshold. \
                  If 'greater_or_equal', will threshold any metric greater than or equal to the given threshold.",
    },
    #kwargs
    {
        "name": "method",
        "type": "str",
        "value": class_default["method"],
        "default": class_default["method"],
        "title": "If 'absolute' (default), amplitudes are absolute amplitudes in uV are returned. \
                  If 'relative', amplitudes are returned as ratios between waveform amplitudes and template amplitudes.",
    },
    {
        "name": "peak",
        "type": "str",
        "value": class_default["peak"],
        "default": class_default["peak"],
        "title": "If maximum channel has to be found among negative peaks ('neg'), positive ('pos') or \
                  both ('both' - default).",
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
        "name": "apply_filter",
        "type": "bool",
        "value": class_default["apply_filter"],
        "default": class_default["apply_filter"],
        "title": "If True, recording is bandpass-filtered",
    },
    {
        "name": "freq_min",
        "type": "float",
        "value": class_default["freq_min"],
        "default": class_default["freq_min"],
        "title": "High-pass frequency for optional filter (default 300 Hz).",
    },
    {
        "name": "freq_max",
        "type": "float",
        "value": class_default["freq_max"],
        "default": class_default["freq_max"],
        "title": "Low-pass frequency for optional filter (default 6000 Hz).",
    },
    {
        "name": "save_property_or_features",
        "type": "bool",
        "value": class_default["save_property_or_features"],
        "default": class_default["save_property_or_features"],
        "title": "If True, it will save features in the sorting extractor.",
    },
    {
        "name": "recompute_info",
        "type": "bool",
        "value": class_default["recompute_info"],
        "default": class_default["recompute_info"],
        "title": "If True, waveforms are recomputed.",
    },
    {
        "name": "max_spikes_per_unit",
        "type": "int",
        "value": class_default["max_spikes_per_unit"],
        "default": class_default["max_spikes_per_unit"],
        "title": "The maximum number of spikes to extract per unit.",
    },
]