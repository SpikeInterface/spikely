"""Test functionality associated with config.py"""

import sys
import random

from PyQt5 import QtWidgets

from spikely import config
from spikely.elements.recording_extractor import RecordingExtractor
from spikely.spikely_main import SpikelyMainWindow


def test_element_conversion():
    """Test the methods used to enable JSON coding/decoding.

    Before JSON encoding, a SpikeElement is converted into a data-based
    dictionary representation using cvt_elem_to_dict().  After JSON decoding,
    the resultant dictionary is re-instantiated as a SpikeElement using
    cvt_dict_to_elem().

    This test runs through both conversions back-to-back and compares the
    resultant SpikeElement with the original SpikeElement to ensure identity.

    """
    cls_list = RecordingExtractor.get_installed_spif_cls_list()
    elem = RecordingExtractor(
        cls_list[random.randint(0, len(cls_list) - 1)]
    )
    elem_dict = config.cvt_elem_to_dict(elem)
    new_elem = config.cvt_dict_to_elem(elem_dict)

    print(f'SpikeElement tested: {elem.display_name}')

    assert (
        elem.__class__.__name__ == new_elem.__class__.__name__
        and elem.__module__ == new_elem.__module__
        and elem.spif_class.__name__ == new_elem.spif_class.__name__
        and elem.param_list == new_elem.param_list
        )


def test_get_main_window():
    """Tests function that finds reference to app's main window."""
    app = QtWidgets.QApplication(sys.argv)  # noqa: F841
    win = SpikelyMainWindow()
    found_win = config.get_main_window()

    assert win is found_win
