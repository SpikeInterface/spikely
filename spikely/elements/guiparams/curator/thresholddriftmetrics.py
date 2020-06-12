from spiketoolkit.curation import threshold_drift_metrics

spif_init_func = threshold_drift_metrics

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
    {
        "name": "metric_name",
        "type": "str",
        "value": "max_drift",
        "default": "max_drift",
        "title": "The name of the drift metric to be thresholded (either 'max_drift' or 'cumulative_drift').",
    },
    {
        "name": "drift_metrics_interval_s",
        "type": "float",
        "value": 51.0,
        "default": 51.0,
        "title": "Time period for evaluating drift.",
    },
    {
        "name": "drift_metrics_min_spikes_per_interval",
        "type": "int",
        "value": 10,
        "default": 10,
        "title": "Minimum number of spikes for evaluating drift metrics per interval.",
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
        "name": "grouping_property",
        "type": "str",
        "value": None,
        "default": None,
        "title": "Property to group channels. E.g. if the recording extractor has the 'group' property and \
                 'grouping_property' is 'group', then waveforms are computed group-wise.",
    },
    {
        "name": "ms_before",
        "type": "float",
        "value": 3.,
        "default": 3.,
        "title": "Time period in ms to cut waveforms before the spike events.",
    },
    {
        "name": "ms_after",
        "type": "float",
        "value": 3.,
        "default": 3.,
        "title": "Time period in ms to cut waveforms after the spike events.",
    },
    {
        "name": "dtype",
        "type": "dtype",
        "value": None,
        "default": None,
        "title": "The numpy dtype of the waveforms.",
    },
    {
        "name": "compute_property_from_recording",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If True and 'grouping_property' is given, the property of each unit is assigned as the corresponding \
                  property of the recording extractor channel on which the average waveform is the largest.",
    },
    {
        "name": "max_channels_per_waveforms",
        "type": "int",
        "value": None,
        "default": None,
        "title": " Maximum channels per waveforms to return. If None, all channels are returned.",
    },
    {
        "name": "n_jobs",
        "type": "int",
        "value": None,
        "default": None,
        "title": "Number of parallel jobs (default None).",
    },
    {
        "name": "memmap",
        "type": "bool",
        "value": True,
        "default": True,
        "title": "If True, waveforms are saved as memmap object (recommended for long recordings with many channels).",
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
    {
        "name": "seed",
        "type": "int",
        "value": 0,
        "default": 0,
        "title": "Random seed for reproducibility.",
    },
    {
        "name": "verbose",
        "type": "bool",
        "value": False,
        "default": False,
        "title": "If True, output from SpikeInterface element is verbose when run.",
    },
]