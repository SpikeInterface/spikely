from spiketoolkit.validation.quality_metric_classes.parameter_dictionaries import (
    get_validation_params,
)
from spiketoolkit.curation import threshold_num_spikes
spif_init_func = threshold_num_spikes
class_default = get_validation_params()

gui_params = [
    {
        "name": "threshold",
        "type": "int",
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
        "name": "sampling_frequency",
        "type": "float",
        "value": None,
        "default": None,
        "title": "The sampling frequency of the result. If None, will check to see if sampling frequency is in sorting extractor.",
    },
    # kwargs
    {
        "name": "save_property_or_features",
        "type": "bool",
        "value": class_default["save_property_or_features"],
        "default": class_default["save_property_or_features"],
        "title": "If True, it will save features in the sorting extractor.",
    },
    {
        "name": "verbose",
        "type": "bool",
        "value": class_default["verbose"],
        "default": class_default["verbose"],
        "title": "If True, output from SpikeInterface element is verbose when run.",
    },
]
