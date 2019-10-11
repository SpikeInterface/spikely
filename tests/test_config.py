import sys

from PyQt5 import QtWidgets

from spikely import config as cfg
from spikely.elements.recording_extractor import RecordingExtractor
from spikely.spikely_main import SpikelyMainWindow


def test_element_conversion():
    cls_list = RecordingExtractor.get_installed_spif_cls_list()
    elem = RecordingExtractor(cls_list[0])
    elem_dict = cfg.cvt_elem_to_dict(elem)
    new_elem = cfg.cvt_dict_to_elem(elem_dict)

    assert (
        elem.__class__.__name__ == new_elem.__class__.__name__
        and elem.__module__ == new_elem.__module__
        and elem.spif_class.__name__ == new_elem.spif_class.__name__
        and elem.param_list == new_elem.param_list
        )


def test_get_main_window():
    app = QtWidgets.QApplication(sys.argv)  # noqa: F841
    win = SpikelyMainWindow()
    found_win = cfg.get_main_window()

    assert win is found_win
