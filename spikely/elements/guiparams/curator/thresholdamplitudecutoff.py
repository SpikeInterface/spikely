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
        "value": "absolute",
        "default": "absolute",
        "title": "If 'absolute' (default), amplitudes are absolute amplitudes in uV are returned. \
                  If 'relative', amplitudes are returned as ratios between waveform amplitudes and template amplitudes.",
    },
    {
        "name": "method",
        "type": "str",
        "value": "absolute",
        "default": "absolute",
        "title": "If 'absolute' (default), amplitudes are absolute amplitudes in uV are returned. \
                  If 'relative', amplitudes are returned as ratios between waveform amplitudes and template amplitudes.",
    },
    {
        "name": "peak",
        "type": "str",
        "value": "both",
        "default": "both",
        "title": "If maximum channel has to be found among negative peaks ('neg'), positive ('pos') or \
                  both ('both' - default).",
    },
    {
        "name": "frames_before",
        "type": "int",
        "value": 3,
        "default": 3,
        "title": "Frames before peak to compute amplitude.",
    },
    {
        "name": "frames_after",
        "type": "int",
        "value": 3,
        "default": 3,
        "title": "Frames after peak to compute amplitude.",
    },
    {
        "name": "apply_filter",
        "type": "bool",
        "value": True,
        "default": True,
        "title": "If True, recording is bandpass-filtered",
    },
    {
        "name": "freq_min",
        "type": "float",
        "value": 300.0,
        "default": 300.0,
        "title": "High-pass frequency for optional filter (default 300 Hz).",
    },
    {
        "name": "freq_max",
        "type": "float",
        "value": 6000.0,
        "default": 6000.0,
        "title": "Low-pass frequency for optional filter (default 6000 Hz).",
    },
    {
        "name": "save_property_or_features",
        "type": "bool",
        "value": True,
        "default": True,
        "title": "If True, it will save features in the sorting extractor.",
    },
    {
        "name": "recompute_info",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If True, waveforms are recomputed.",
    },
    {
        "name": "max_spikes_per_unit",
        "type": "int",
        "value": 300,
        "default": 300,
        "title": "The maximum number of spikes to extract per unit.",
    },
]
